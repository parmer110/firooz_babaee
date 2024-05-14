from django.conf import settings
import os
from lxml import etree as ET
import re
from datetime import datetime
from django.core.exceptions import ValidationError
from config.logging_setup import log_error
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from companies.models import Company
from products.models import Product
from order.models import XMLFile as model_OD, Orders as model_ODD
from barcode.models import Barcode as model_Barcode

class XMLAnalyzer:
    def __init__(self):
        self.odd_instances = []
        self.barcode_instances = []

    def count_tags(self, root, target_tag):
        return sum(1 for _ in root.iter(target_tag))

    def validate_and_extract(self, bc):
        if len(bc) < 49 or len(bc) > 68:
            raise ValueError("Invalid barcode length.")

        pattern = (
            r'^01(\d{14})'
            r'21(\d{20})'
            r'17(\d{6})'
            r'10([ -~]{1,20})$'
        )

        match = re.match(pattern, bc)
        if not match:
            err_message = f"{bc}'s Barcode format is incorrect."
            log_error(err_message)
            return Response({"error": err_message}, status=status.HTTP_400_BAD_REQUEST)

        gtin = match.group(1)
        uid = match.group(2)
        exp = match.group(3)
        lot = match.group(4)

        level_id = gtin[0]
        if level_id != uid[5]:
            err_message = f"{bc}'s Level ID does not match the required condition."
            log_error(err_message)
            return Response({"error": err_message}, status=status.HTTP_400_BAD_REQUEST)

        prefix = uid[:5]

        parts = {
            "gtin": gtin[1:],
            "uid": uid,
            "exp": exp,
            "lot": lot,
            "level_id": level_id,
            "prefix": prefix
        }

        return parts

    def parse_string_with_regex(self, bc, px, exp, lot):
        err = []

        regex_pattern = r'^01(\d{14})21(\d{20})17(\d{6})10(.{1,20})$'

        match = re.match(regex_pattern, bc)
        if match:
            tcgtin = match.group(1)
            tcuid = match.group(2)
            tcexp = match.group(3)
            tclot = match.group(4)

            if tclot != lot:
                error_message = f"lot barcode({tclot}) is not equal to {lot}."
                log_error(error_message)
                err.append(error_message)
            if tcexp != exp:
                error_message = f"exp barcode({tcexp}) is not equal to {exp}."
                log_error(error_message)
                err.append(error_message)
            if not tcuid.startswith(px):
                error_message = f"Company prefix({tcuid[:len(px)]}) is not equal to ({px})."
                log_error(error_message)
                err.append(error_message)

            if len(tclot) > 20:
                error_message = "Element 4 should not exceed 20 characters."
                log_error(error_message)
                err.append(error_message)

            if not err:
                return True, {'gtin': tcgtin, 'uid': tcuid, 'exp': tcexp, 'lot': tclot}
            else:
                return False, err
        else:
            error_message = f"Structure error: Invalid {bc} format."
            return False, [error_message]

    def irc_gtin_validation(self, parent, root=None, parent_gtin=None, irc=None, parent_level_id=None):
        if root is None:
            root = parent

        level_id = parent_level_id

        if root.tag in ["SP", "TC"]:
            bc = root.attrib.get("PBC" if root.tag == "SP" else "BC")
            extracted_data = self.validate_and_extract(bc)
            if extracted_data is None:
                return None, None, None
            gtin = extracted_data['gtin']
            level_id = extracted_data['level_id']

            if parent_gtin and gtin != parent_gtin:
                err_message = f"{root}'s barcode does not match the constant GTIN in {parent}"
                log_error(err_message)
                return None, None, None
            
            parent_gtin = gtin
            if parent.tag == "ODD":
                irc = parent.attrib.get("SC", "")

        else:
            if root.tag != "ODD":
                err_message = f"{root.tag} is not a valid XML tag under {parent.tag}'s parent. Structure error!"
                log_error(err_message)
                return None, None, None

        for child in root:
            result = self.irc_gtin_validation(root, child, parent_gtin, irc, level_id)
            if result == (None, None, None):
                return None, None, None
            irc, parent_gtin, level_id = result

        return irc, parent_gtin, level_id

    def OD(self, root, parent, OD_instance=None, ODD_instance=None, parent_sp=None):
        TC_count = self.count_tags(root, "TC")
        no = root.attrib.get('NO')
        if int(no) == TC_count:
            return parent
        else:
            error_message = f"OD NO property error! The {no} which is reported is not equal {TC_count} that already exists"
            log_error(error_message)
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

    def ODD(self, root, parent, OD_instance=None, ODD_instance=None, parent_sp=None):
        TC_count = self.count_tags(root, "TC")
        no = root.attrib.get('NO')
        sc = root.attrib.get('SC')
        md = root.attrib.get('MD')
        ed = root.attrib.get('ED')
        bn = root.attrib.get('BN')
        lc = root.attrib.get('LC')
        oc = OD_instance.SupplierCode
        odd_instance = model_ODD()

        if int(no) != TC_count:
            error_message = f"ODD NO property error! The {odd_instance.no} which is reported is not equal {TC_count} that already exists"
            log_error(error_message)
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        irc, gtin, level_id = self.irc_gtin_validation(root)

        if irc and gtin:
            full_gtin = level_id + gtin
            product, created = Product.objects.get_or_create(
                GTIN=full_gtin,
                defaults={
                    'ProductFrName': "",
                    'irc': irc,
                    'ProducerCompanyCode': oc
                }
            )
        else:
            error_message = f"There is no IRC or GTIN exitst in {root}."
            log_error(error_message)
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        date_object = datetime.strptime(ed, '%Y-%m-%d')
        formatted_date = date_object.strftime('%y%m%d')

        odd_instance.xmlfile_id = parent
        odd_instance.ProductCode = product
        odd_instance.NumberOfOrder = no
        odd_instance.BatchNumber = bn
        odd_instance.ProduceDate = md
        odd_instance.ExpDate = formatted_date
        odd_instance.LicenceCode = lc

        self.odd_instances.append(odd_instance)

        return odd_instance

    def SP(self, root, parent, OD_instance, ODD_instance, parent_sp=None):
        od_px = OD_instance.SupplierCode.Prefix
        odd_ed = ODD_instance.ExpDate
        odd_bn = ODD_instance.BatchNumber
        pbc = root.attrib.get('PBC')

        barcode_instance = model_Barcode()
        sit, bc = self.parse_string_with_regex(pbc, od_px, odd_ed, odd_bn)

        if sit:
            if isinstance(ODD_instance, model_ODD):
                barcode_instance.orderid = ODD_instance
            if isinstance(parent_sp, model_Barcode):
                barcode_instance.parent = parent_sp.uuid

            barcode_instance.uuid = bc['uid']
            barcode_instance.levelid = bc['gtin'][0]
            barcode_instance.RndEsalat = None

            self.barcode_instances.append(barcode_instance)

            return barcode_instance
        else:
            log_error(bc)
            print(bc)
            return bc

    def TC(self, root, parent, OD_instance, ODD_instance, parent_sp=None):
        od_px = OD_instance.SupplierCode.Prefix
        odd_ed = ODD_instance.ExpDate
        odd_bn = ODD_instance.BatchNumber
        bc = root.attrib.get('BC')

        barcode_instance = model_Barcode()
        sit, bc = self.parse_string_with_regex(bc, od_px, odd_ed, odd_bn)

        if sit:
            if isinstance(ODD_instance, model_ODD):
                barcode_instance.orderid = ODD_instance
            if isinstance(parent_sp, model_Barcode):
                barcode_instance.parent = parent_sp.uuid

            barcode_instance.uuid = bc['uid']
            barcode_instance.levelid = bc['gtin'][0]
            barcode_instance.RndEsalat = root.attrib.get('HC')

            self.barcode_instances.append(barcode_instance)
        else:
            log_error(bc)
            return bc

    def traverse_xml(self, root, parent, OD_instance=None, ODD_instance=None, parent_sp=None):
        tag_functions = {
            'OD': self.OD,
            'ODD': self.ODD,
            'SP': self.SP,
            'TC': self.TC
        }
        try:
            if root.tag in tag_functions:
                instance = tag_functions[root.tag](root, parent, OD_instance, ODD_instance, parent_sp)
                if root.tag == "OD":
                    OD_instance = instance
                elif root.tag == "ODD":
                    ODD_instance = instance
                elif root.tag == "SP":
                    parent_sp = instance
            else:
                log_error("No function defined for tag:", root.tag)
                return {"error": f"No function defined for tag: {root.tag}"}, False

            for child in root:
                result, success = self.traverse_xml(child, instance, OD_instance, ODD_instance, parent_sp)
                if not success:
                    return result, False

            return {"success": "XML processed successfully"}, True
        except Exception as e:
            log_error(str(e))
            return {"error": str(e)}, False

    def process_xml(self, file_obj, xml_instance):
        context = ET.iterparse(file_obj, events=("end",), tag="OD")
        for event, elem in context:
            result, success = self.traverse_xml(elem, xml_instance)
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

            if not success:
                return result

        if result['success']:
            model_ODD.objects.bulk_create(self.odd_instances)
            model_Barcode.objects.bulk_create(self.barcode_instances)

        return result
