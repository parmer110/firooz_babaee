from django.conf import settings
import os
import xml.etree.ElementTree as ET
import re
from django.core.exceptions import ValidationError
from config.logging_setup import log_error
from rest_framework.response import Response
from rest_framework import status
# from common.models import XMLFile, OD as model_OD, ODD as model_ODD, SP as model_SP, TC as model_TC, Barcode as model_Barcode
from order.models import tblXmlOrders as model_OD, tblOrder as model_ODD
from barcode.models import Barcode as model_Barcode


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
    # exp = exp.replace("-", "")[2:]

    # Define regular expression patterns
    regex_patterns = [
        r'^01(\d{14})21(\d{20})17(\d{6})10([0-9a-zA-Z]{1,20})\s*$',  # General pattern with optional whitespace at the end
        r'^01(\d{14})',        # Element 1: gtin (starts with "01" and 14 digits)
        r'^21(\d{20})',        # Element 2: uid (starts with "21" and 20 digits)
        r'^17(\d{6})',         # Element 3: exp (starts with "17" and 6 digits)
        r'^10([0-9a-zA-Z]{1,20})$'  # Element 4: remaining until the end (starts with "10" and anything after that)
    ]

    # Search for elements using regular expressions
    match = re.match(regex_patterns[0], bc)
    if match:
        # Extract element values
        tcgtin = match.group(1)
        tcuid = match.group(2)
        tcexp = match.group(3)
        tclot = match.group(4)

        # Check the type of elements and append errors to the err list if any
        if not tcgtin.isdigit():
            err.append(f"gtin of bc({bc}) should be of type numeric.")
        if not tcuid.isdigit():
            err.append(f"uid of bc({bc}) should be of type numeric.")
        if not tcexp.isdigit():
            err.append(f"exp of bc({bc}) should be of type numeric.")
        if not tclot.isalnum():
            err.append(f"lot of bc ({bc}) should be of type alphanumeric.")

        # Check lot and exp and prefix values and append errors to the err list if any
        if tclot != lot:
            err.append(f"lot barcode({tclot}) is not equal to {lot}.")
        if tcexp != exp:
            err.append(f"exp barcode({tcexp}) is not equal to {exp}.")
        if not tcuid.startswith(px):
            err.append(f"Company prefix({tcuid[:5]}) is not equal to ({px}).")

        # Check the length of element 4 and append errors to the err list if any
        if len(tclot) > 20:
            err.append("Element 4 should not exceed 20 characters.")

        # gtin validation checking

        # Return the values if successful

        result = {'gtin': tcgtin, 'uid': tcuid, 'exp': tcexp, 'lot': tclot}
        if not err:
            return True, {'gtin': tcgtin, 'uid': tcuid, 'exp': tcexp, 'lot': tclot}
        else:
            return False, err

    else:
        return False, [f"Structure error: Invalid {bc} format."]


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

    TC_count = count_tags(root, "TC")
    
    od_instance = model_OD()

    od_instance.xml_file = parent
    od_instance.no = root.attrib.get('NO')
    if int(od_instance.no) != TC_count:
        error_message = f"OD NO property error! The {od_instance.no} which is reported is not equal {TC_count} that already exists"
        log_error(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    od_instance.dc = root.attrib.get('DC')
    od_instance.oc = root.attrib.get('OC')
    od_instance.lc = root.attrib.get('LC')
    od_instance.px = root.attrib.get('PX')
    od_instance.wo = root.attrib.get('WO')
    
    od_instance.save()
    return od_instance

# Order details xml tags handling
def ODD(root, parent, OD_instance=None, ODD_instance=None, parent_sp=None):

    TC_count = count_tags(root, "TC")

    odd_instance = model_ODD()
    odd_instance.od = parent
    odd_instance.no = root.attrib.get('NO')
    if int(odd_instance.no) != TC_count:
        error_message = f"ODD NO property error! The {odd_instance.no} which is reported is not equal {TC_count} that already exists"
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        log_error(error_message)
    odd_instance.md = root.attrib.get('MD')
    odd_instance.ed = root.attrib.get('ED')
    odd_instance.sc = root.attrib.get('SC')
    odd_instance.bn = root.attrib.get('BN')
    odd_instance.lc = root.attrib.get('LC')

    odd_instance.save()
    return odd_instance

# Specification Pack xml tags handling
def SP(root, parent, OD_instance, ODD_instance, parent_sp=None):

    od_px = OD_instance.px
    odd_ed = ODD_instance.ed
    odd_bn = ODD_instance.bn

    # Barcode
    barcode_instance = model_Barcode()
    sit, bc = parse_string_with_regex(root.attrib.get('PBC'), od_px, odd_ed, odd_bn)

    if sit:
        # Ensure that parent_sp is an instance of SP
        if isinstance(ODD_instance, model_ODD):
            barcode_instance.production_order = ODD_instance
        if isinstance(parent_sp, model_Barcode):
            barcode_instance.parent = parent_sp
        barcode_instance.gtin = bc['gtin']
        barcode_instance.uid = bc['uid']
        barcode_instance.exp = bc['exp']
        barcode_instance.lot = bc['lot']
        barcode_instance.hc = None

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

    # Barcode
    barcode_instance = model_Barcode()
    sit, bc = parse_string_with_regex(root.attrib.get('BC'), od_px, odd_ed, odd_bn)

    if sit:
        # Ensure that parent_sp is an instance of SP
        if isinstance(parent_sp, model_Barcode):
            barcode_instance.parent = parent_sp
        barcode_instance.production_order = ODD_instance
        barcode_instance.gtin = bc['gtin']
        barcode_instance.uid = bc['uid']
        barcode_instance.exp = bc['exp']
        barcode_instance.lot = bc['lot']
        barcode_instance.hc = root.attrib.get('HC')

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
