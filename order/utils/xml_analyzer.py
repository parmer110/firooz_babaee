from django.conf import settings
import os
import xml.etree.ElementTree as ET
import re
from django.core.exceptions import ValidationError
from config.logging_setup import log_error
from rest_framework.response import Response
from rest_framework import status
from companies.models import Company
from products.models import Product
from order.models import XMLFile as model_OD, Orders as model_ODD
from barcode.models import Barcode as model_Barcode

def count_tags(root, target_tag):
    count = 0
    if root.tag == target_tag:
        count += 1
    for child in root:
        count += count_tags(child, target_tag)
    return count        

def validate_and_extract(bc):
    # اعتبارسنجی طول کلی
    if len(bc) < 49 or len(bc) > 68:
        raise ValueError("Invalid barcode length.")

    # تعریف الگوهای انطباقی برای هر جزء
    pattern = (
        r'^01(\d{14})'
        r'21(\d{20})'
        r'17(\d{6})'
        r'10([ -~]{1,20})$'  # این الگو از 1 تا 20 کاراکتر قابل چاپ ascii را شامل می‌شود
    )

    # اجرای الگوی منظم بر روی رشته
    match = re.match(pattern, bc)
    if not match:
        err_message = r"{bc}'s Barcode format is incorrect."
        log_error(err_message)
        return Response({"error": err_message}, status=status.HTTP_400_BAD_REQUEST)

    # استخراج اجزا
    gtin = match.group(1)
    uid = match.group(2)
    exp = match.group(3)
    lot = match.group(4)

    # استخراج و بررسی level_id
    level_id = gtin[0]
    if level_id != uid[5]:
        err_message = r"{bc}'s Level ID does not match the required condition."
        log_error(err_message)
        return Response({"error": err_message}, status=status.HTTP_400_BAD_REQUEST)

    # استخراج prefix
    prefix = uid[:5]

    # دیکشنری از اجزای استخراج شده
    parts = {
        "gtin": gtin[1:],
        "uid": uid,
        "exp": exp,
        "lot": lot,
        "level_id": level_id,  # کاراکتر اول جزء gtin
        "prefix": prefix       # پنج کاراکتر اول جزء uid
    }

    return parts

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

# IRC accross GTIN validation - recursively
def irc_gtin_validation(parent, root=None, parent_gtin=None, irc=None):
    if root is None:
        root = parent  # Start with parent if root is not provided

    if root.tag in ["SP", "TC"]:
        bc = root.attrib.get("PBC" if root.tag == "SP" else "BC")
        extracted_data = validate_and_extract(bc)
        if extracted_data is None:
            return None, None  # Early exit if extraction fails
        gtin = extracted_data['gtin']

        if parent_gtin and gtin != parent_gtin:
            err_message = f"{root}'s barcode does not match the constant GTIN in {parent}"
            log_error(err_message)
            return None, None  # Stop recursion and report error
        
        parent_gtin = gtin  # Update parent_gtin with the new GTIN
        if parent.tag == "ODD":
            irc = parent.attrib.get("SC", "")

    else:
        if root.tag != "ODD":
            err_message = f"{root.tag} is not a valid XML tag under {parent.tag}'s parent. Structure error!"
            log_error(err_message)
            return None, None

    for child in root:
        result = irc_gtin_validation(root, child, parent_gtin, irc)
        if result == (None, None):
            return None, None  # Propagate early exits up the call stack
        irc, parent_gtin = result  # Update irc and parent_gtin after each child

    return irc, parent_gtin

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
    no = root.attrib.get('NO')
    # Count of TC elements are child of this order
    if int(no) == TC_count:
        return parent
    else:
        error_message = f"OD NO property error! The {no} which is reported is not equal {TC_count} that already exists"
        log_error(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

# Order details xml tags handling
def ODD(root, parent, OD_instance=None, ODD_instance=None, parent_sp=None):
    
    # Initialization
    TC_count = count_tags(root, "TC")
    no = root.attrib.get('NO')
    sc = root.attrib.get('SC')
    md = root.attrib.get('MD')
    ed = root.attrib.get('ED')
    bn = root.attrib.get('BN')
    lc = root.attrib.get('LC')
    oc = OD_instance.SupplierCode
    odd_instance = model_ODD()
    
    # Data validation control :: Num of tc components
    if int(no) == TC_count:
        odd_instance.NumberOfOrder = no
    else:
        error_message = f"ODD NO property error! The {odd_instance.no} which is reported is not equal {TC_count} that already exists"
        log_error(error_message)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
    
    # Data validation control :: GTIN accross IRC validation.
    irc, gtin = irc_gtin_validation(root)
    
    if irc and gtin:
        product, created = Product.objects.get_or_create(
            GTIN=gtin,
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
    
    # Data assignment
    odd_instance.xmlfile_id = parent
    odd_instance.ProductCode = product
    odd_instance.NumberOfOrder = no
    odd_instance.BatchNumber = bn
    odd_instance.ProduceDate = md
    odd_instance.ExpDate = ed
    odd_instance.LicenceCode = lc

    # INSERT instance to database
    odd_instance.save()
    return odd_instance

# Specification Pack xml tags handling
def SP(root, parent, OD_instance, ODD_instance, parent_sp=None):

    # Initialize
    od_px = OD_instance.SupplierCode.Prefix
    odd_ed = ODD_instance.ExpDate
    odd_bn = ODD_instance.BatchNumber
    pbc = root.attrib.get('PBC')

    # Barcode
    barcode_instance = model_Barcode()
    sit, bc = parse_string_with_regex(pbc, od_px, odd_ed, odd_bn)

    if sit:
        # Ensure that parent_sp is an instance of SP
        if isinstance(ODD_instance, model_ODD):
            barcode_instance.orderid = ODD_instance
        if isinstance(parent_sp, model_Barcode):
            barcode_instance.parent = parent_sp.uuid
        # barcode_instance.gtin = bc['gtin']
        barcode_instance.uuid = bc['uid']
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
    
    od_px = OD_instance.SupplierCode.Prefix
    odd_ed = ODD_instance.ExpDate
    odd_bn = ODD_instance.BatchNumber
    bc = root.attrib.get('BC')

    # Barcode
    barcode_instance = model_Barcode()
    sit, bc = parse_string_with_regex(bc, od_px, odd_ed, odd_bn)

    if sit:
        # Ensure that parent_sp is an instance of SP
        if isinstance(ODD_instance, model_ODD):
            barcode_instance.orderid = ODD_instance
        # Ensure that parent_sp is an instance of SP
        if isinstance(parent_sp, model_Barcode):
            barcode_instance.parent = parent_sp.uuid
        # barcode_instance.gtin = bc['gtin']
        barcode_instance.uuid = bc['uid']
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
            result, success = traverse_xml(child, instance, OD_instance, ODD_instance, parent_sp)
            if not success:
                return result, False

        return {"success": "XML processed successfully"}, True
    except Exception as e:
        log_error(str(e))
        return {"error": str(e)}, False

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
