import os
from lxml import etree as ET
import hashlib
import random
import string
import datetime
from persiantools.jdatetime import JalaliDateTime

def generate_random_alphanum_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_random_numeric_string(length):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_random_date(start_date, end_date):

    random_number_of_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def ODs (OD_max):
    px_exp_lot = []
    for i in range(OD_max):
        px = 44453# random.randint(10000, 99999)
        exp = str(generate_random_date(datetime.date(2025, 1, 1), datetime.date(2028, 1, 1)))
        exp = exp.replace("-", "")[-6:]
        lot_length = random.randint(1, 5)
        lot = generate_random_alphanum_string(lot_length)

        px_exp_lot_dict = {"px": str(px), "exp": str(exp), "lot": lot}
        px_exp_lot.append(px_exp_lot_dict)
    return px_exp_lot

def generate_xml_with_tags(file_name, OD_max=1, ODD_max=2, SP_max=4, TC_max=20):
    # px_exp_lot is a list of dictionaries with px, exp and lot keys

    # Variable initialization
    tc_odd_count = 0
    tc_od_count = 0

    # بدست آوردن مسیر کنونی فایل
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # ایجاد پوشه اگر وجود نداشته باشد
    result_dir = os.path.join(current_dir, "TC_maker_results")
    create_directory(result_dir)

    # تاریخ و زمان محلی
    local_time = JalaliDateTime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # تعیین نام فایل XML با استفاده از تاریخ و زمان محلی
    xml_file_name = f"{local_time}.xml"

    # تعیین مسیر فایل XML
    xml_file_path = os.path.join(result_dir, xml_file_name)
    
    # ایجاد ریشه اصلی برای فایل XML
    # ODs list of dictionaris contais px and exp and lot key-values generator
    ODs_listofdic = ODs(OD_max)
    # OD tag generator
    for OD in ODs_listofdic:
        od = ET.Element("OD")

        px = OD['px']
        exp = OD['exp']
        lot = OD['lot']

        od.set("NO", "0")
        od.set("DC", "*0064416488")
        od.set("OC", "10100651897")
        od.set("LC", "")
        od.set("PX", px)
        od.set("WO", "6")

        num_ODD = random.randint(1, ODD_max)

        # ODD tag generator
        for i in range(num_ODD):
            # ODD tag
            odd = ET.SubElement(od, "ODD")

            odd.set("NO", "0")
            odd.set("MD", "2024-02-01")
            odd.set("ED", exp)
            odd.set("SC", "1331226614962095")
            odd.set("BN", lot)
            odd.set("LC", "")

            random_gtin = generate_random_numeric_string(13)

            num_SPs = random.randint(1, SP_max)
            # SP tag generator
            for i in range(num_SPs):
                sp_tag = ET.SubElement(odd, "SP")
                # SP level generator
                num_SP = random.randint(0, 8)

                level_id = num_SP - i
                random_uid = generate_random_numeric_string(14)
                bc_value = f"01{level_id}{random_gtin}21{px}{level_id}{random_uid}17{exp}10{lot}"

                sp_tag.set("PBC", bc_value)

                for i in range(num_SP):
                    sp_tag = ET.SubElement(sp_tag, "SP")
                    
                    level_id = num_SP - i
                    random_uid = generate_random_numeric_string(14)
                    bc_value = f"01{level_id}{random_gtin}21{px}{level_id}{random_uid}17{exp}10{lot}"

                    sp_tag.set("PBC", bc_value)
                
                    num_TC = random.randint(1, TC_max)
                    
                # TC tag generator
                for i in range(num_TC):

                    tc_odd_count += 1
                    tc_od_count += 1

                    # ایجاد تگ TC
                    tc_tag = ET.SubElement(sp_tag, "TC")

                    random_uid = generate_random_numeric_string(14)
                    level_id = 0
                    bc_value = f"01{level_id}{random_gtin}21{px}{level_id}{random_uid}17{exp}10{lot}"
                    hsc_value = generate_random_numeric_string(16)
                    hc_hash = hashlib.sha1(hsc_value.encode()).hexdigest().upper()

                    # اضافه کردن مشخصات HC، BC و HSC به تگ TC
                    tc_tag.set("HC", hc_hash)
                    tc_tag.set("BC", bc_value)
                    tc_tag.set("HSC", hsc_value)

            # TC tag generator
            for i in range(num_TC):

                tc_odd_count += 1
                tc_od_count += 1

                # ایجاد تگ TC
                tc_tag = ET.SubElement(sp_tag, "TC")

                random_uid = generate_random_numeric_string(14)
                level_id = 0
                bc_value = f"01{level_id}{random_gtin}21{px}{level_id}{random_uid}17{exp}10{lot}"
                hsc_value = generate_random_numeric_string(16)
                hc_hash = hashlib.sha1(hsc_value.encode()).hexdigest().upper()

                # اضافه کردن مشخصات HC، BC و HSC به تگ TC
                tc_tag.set("HC", hc_hash)
                tc_tag.set("BC", bc_value)
                tc_tag.set("HSC", hsc_value)

            odd.set("NO", str(tc_odd_count))
            tc_odd_count = 0
        od.set("NO", str(tc_od_count))
        tc_od_count = 0
        
        # ایجاد شیوه برای فایل XML
        tree = ET.ElementTree(od)
    
    # ذخیره فایل XML با فرمت مناسب
    tree.write(xml_file_path, encoding="utf-8", xml_declaration=True, pretty_print=True)

# فراخوانی تابع برای ایجاد فایل XML
generate_xml_with_tags("bchc.xml", OD_max=1, ODD_max=3, SP_max=4, TC_max=20)
