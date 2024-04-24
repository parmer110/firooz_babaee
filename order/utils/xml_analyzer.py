from django.conf import settings
import os
import xml.etree.ElementTree as ET
import re
from django.core.exceptions import ValidationError
from config.logging_setup import log_error
from rest_framework.response import Response
from rest_framework import status
# from common.models import XMLFile, OD as model_OD, ODD as model_ODD, SP as model_SP, TC as model_TC, Barcode as model_Barcode
from order.models import WarehouseOrder as model_OD, tblOrder as model_ODD
from companies.models import Company
from barcode.models import Barcode as model_Barcode
from products.models import Product


def count_tags(root, target_tag):
    count = 0
    if root.tag == target_tag:
        count += 1
    for child in root:
        count += count_tags(child, target_tag)
    return count        

# Extracting BC values and validation checking
def parse_string_with_regex(bc, px, exp, lot):
    err = []

    # Modify the input exp for comparison with tcexp
    exp = exp.replace("-", "")[2:]

    # Define the correct regular expression pattern
    regex_pattern = r'^01(\d{14})21(\d{20})17(\d{6})10(.{1,20})$'

    # Search for elements using the regular expression
    match = re.match(regex_pattern, bc)
    if match:
        # Extract element values
        tcgtin = match.group(1)
        tcuid = match.group(2)
        tcexp = match.group(3)
        tclot = match.group(4)

        # Append errors if the type checks or values do not match
        if tclot != lot:
            error_message = f"lot barcode({tclot}) is not equal to {lot}."
            log_error(f"lot barcode({tclot}) is not equal to {lot}.")
            err.append(error_message)
        if tcexp != exp:
            error_message = f"exp barcode({tcexp}) is not equal to {exp}."
            log_error(f"exp barcode({tcexp}) is not equal to {exp}.")
            err.append(error_message)
        if not tcuid.startswith(px):
            error_message = f"Company prefix({tcuid[:len(px)]}) is not equal to ({px})."
            log_error(error_message)
            err.append(error_message)

        # Check the length of element 4 and append errors if any
        if len(tclot) > 20:
            error_message = "Element 4 should not exceed 20 characters."
            log_error(error_message)
            err.append(error_message)

        # Return the values if successful
        if not err:
            return True, {'gtin': tcgtin, 'uid': tcuid, 'exp': tcexp, 'lot': tclot}
        else:
            return False, err
    else:
        error_message = f"Structure error: Invalid {bc} format."
        return False, [error_message]

# XML validation representation functions
def ODv(root, parent):
    error_message = None
    TC_count = count_tags(root, "TC")
    NO_count = root.attrib.get('NO')
    if NO_count.no != TC_count:
        error_message = f"OD NO property error! The {NO_count} which is reported is not equal {TC_count} that already exists"
    return error_message, root

def ODDv(root, parent):
    error_message = None
    TC_count = count_tags(root, "TC")
    ODD_count = root.attrib.get('NO')
    if ODD_count != TC_count:
        error_message = f"ODD NO property error! The {ODD_count} which is reported is not equal {TC_count} that already exists"
    return error_message, root

def SPv(root, parent):
    error_message = None
    OD_PX = root.attrib.get('PX')
    return error_message, root
def TCv(root, parent):
    error_message = None
    return error_message, root

# Order xml tags handling
def OD(root, parent, OD_instance=None, ODD_instance=None, parent_sp=None):

    # Initialization
    TC_count = count_tags(root, "TC")
    no = root.attrib.get('NO')
    dc = root.attrib.get('DC')
    oc = root.attrib.get('OC')
    px = root.attrib.get('PX')
    wo = root.attrib.get('WO')
    
    # Reference model object
    od_instance = model_OD()
    
    # Reference XML file    
    od_instance.orderid = parent
    
    # Count of TC elements are child of this order
    if int(no) == TC_count:
        od_instance.no = no
    else:
        error_message = f"OD NO property error! The {od_instance.no} which is reported is not equal {TC_count} that already exists"
        log_error(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    
    # Distributor company nid assignment
    if Company.objects.filter(nationalid=dc).exists():
        od_instance.distributercompanynid = Company.objects.get(nationalid=dc)
    else:
        error_message = f"No system registered company with {dc} nid, Please upgrade companies registration."
        log_error(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    
    # Order companies nid assignment
    if Company.objects.filter(nationalid=oc).exists():
        od_instance.ordercompanynid = Company.objects.get(nationalid=oc)
    else:
        error_message = f"No system registered company with {oc} nid, Please upgrade companies registration."
        log_error(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    od_instance.lc = root.attrib.get('LC')

    # Order company Prefix
    if Company.objects.filter(prefix=px).exists():
        od_instance.px = px
    else:
        error_message = f"The prefix {px} is not existed within system companies registration."
        log_error(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    
    od_instance.wo = wo

    od_instance.save()
    return od_instance

# Order details xml tags handling
def ODD(root, parent, OD_instance=None, ODD_instance=None, parent_sp=None):
    
    # Initialization
    TC_count = count_tags(root, "TC")
    no = root.attrib.get('NO')
    sc = root.attrib.get('SC')

    odd_instance = model_ODD()

    odd_instance.invoicenumber = parent

    if Product.objects.filter(irc=sc).exists():
        odd_instance.GTIN = Product.objects.get(irc=sc)
    else:
        error_message = f"There is no ird: {sc} exitst. Please upgrade produaction table."

    if int(no) == TC_count:
        odd_instance.no = no
    else:
        error_message = f"ODD NO property error! The {odd_instance.no} which is reported is not equal {TC_count} that already exists"
        log_error(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    
    odd_instance.md = root.attrib.get('MD')
    odd_instance.ed = root.attrib.get('ED')
    odd_instance.sc = sc
    odd_instance.bn = root.attrib.get('BN')
    odd_instance.lc = root.attrib.get('LC')

    odd_instance.save()
    return odd_instance

# Specification Pack xml tags handling
def SP(root, parent, OD_instance, ODD_instance, parent_sp=None):

    # Initialize
    od_px = OD_instance.px
    odd_ed = ODD_instance.ed
    odd_bn = ODD_instance.bn
    pbc = root.attrib.get('PBC')

    # Barcode
    barcode_instance = model_Barcode()
    sit, bc = parse_string_with_regex(pbc, od_px, odd_ed, odd_bn)

    if sit:
        # Ensure that parent_sp is an instance of SP
        if isinstance(ODD_instance, model_ODD):
            barcode_instance.order = ODD_instance
        if isinstance(parent_sp, model_Barcode):
            barcode_instance.parent = parent_sp.UUID
        # barcode_instance.gtin = bc['gtin']
        barcode_instance.UUID = bc['uid']
        barcode_instance.levelid = bc['gtin'][0]
        # barcode_instance.exp = bc['exp']
        # barcode_instance.lot = bc['lot']
        barcode_instance.RndEsalat = None

        barcode_instance.save()

        return barcode_instance
    else:
        log_error(bc)
        print(bc)
        return bc

# Tracking code xml tags handling
def TC (root, parent, OD_instance, ODD_instance, parent_sp=None):
    
    od_px = OD_instance.px
    odd_ed = ODD_instance.ed
    odd_bn = ODD_instance.bn
    bc = root.attrib.get('BC')

    # Barcode
    barcode_instance = model_Barcode()
    sit, bc = parse_string_with_regex(bc, od_px, odd_ed, odd_bn)

    if sit:
        # Ensure that parent_sp is an instance of SP
        if isinstance(ODD_instance, model_ODD):
            barcode_instance.order = ODD_instance
        # Ensure that parent_sp is an instance of SP
        if isinstance(parent_sp, model_Barcode):
            barcode_instance.parent = parent_sp.UUID
        # barcode_instance.gtin = bc['gtin']
        barcode_instance.UUID = bc['uid']
        barcode_instance.levelid = bc['gtin'][0]
        # barcode_instance.exp = bc['exp']
        # barcode_instance.lot = bc['lot']
        barcode_instance.RndEsalat = root.attrib.get('HC')

        barcode_instance.save()
    else:
        log_error(bc)
        return bc

# xml tags function representer
tag_functions = {
    'OD': OD,
    'ODD': ODD,
    'SP': SP,
    'TC': TC
}
# xml validation function representer
tag_validate_functions = {
    'OD': ODv,
    'ODD': ODDv,
    'SP': SPv,
    'TC': TCv
}

# Recursive hirerchy xml tags definition.
def traverse_xml(root, parent, OD_instance=None, ODD_instance=None, parent_sp=None):
    if root.tag in tag_functions:
        instance = tag_functions[root.tag](root, parent, OD_instance, ODD_instance, parent_sp)
        if root.tag == "OD":
            OD_instance = instance
        if root.tag == "ODD":
            ODD_instance = instance
        if root.tag == "SP":
            parent_sp = instance

    # xml tags definition validation
    else:
        log_error("No function defined for tag:", root.tag)
        print("No function defined for tag:", root.tag)
        
    for child in root:
        traverse_xml(child, instance, OD_instance, ODD_instance, parent_sp)

# XML file validation checking
def validation_check(root, parent=None, OD_instance=None, ODD_instance=None, parent_sp=None, err_list=None):
    if err_list is None:
        err_list = []

    instance = None
    if root.tag in tag_validate_functions:
        errors, parent = tag_validate_functions[root.tag](root, parent, OD_instance, ODD_instance, parent_sp)

        if errors:
            err_list.append(errors)
        
        # Update the instances based on the tag type
        if root.tag == "OD":
            OD_instance = instance
        elif root.tag == "ODD":
            ODD_instance = instance
        elif root.tag in ["SP", "TC"]:
            parent_sp = instance
        
        # Add errors to the main error list
        err_list.extend(errors)
    else:
        error_message = f"No function defined for tag: {root.tag}"
        err_list.append(error_message)

    for child in root:
        validation_check(child, instance or parent, OD_instance, ODD_instance, parent_sp, err_list)

    return err_list

# parsing xml
def analyze_xml(xml_file, xml_instance):

    tree = ET.parse(xml_file)
    root = tree.getroot()
    traverse_xml(root, xml_instance)
