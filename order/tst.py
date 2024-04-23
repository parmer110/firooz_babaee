# from .models import WarehouseOrder as tblXmlOrders

# def parse_element(element):
#     # check if the element is an OD element
#     if element.tag == "OD":
#         # get the NO, DC, OC, LC, and PX attributes of the OD element
#         no = element.get("NO")
#         dc = element.get("DC")
#         oc = element.get("OC")
#         lc = element.get("LC")
#         px = element.get("PX")
#         # create a new instance of the tblXmlOrders model with these attributes
#         xml_order = tblXmlOrders(no=no, dc=dc, oc=oc, lc=lc, px=px)
#         # save the instance to the database
#         xml_order.save()
#     # check if the element is an ODD element
#     elif element.tag == "ODD":
#         # get the NO, MD, ED, BN, and LC attributes of the ODD element
#         no = element.get("NO")
#         md = element.get("MD")
#         ed = element.get("ED")
#         bn = element.get("BN")
#         lc = element.get("LC")
#         # create a new instance of the tblOrder model with these attributes
#         order = tblOrder(no=no, md=md, ed=ed, bn=bn, lc=lc)
#         # save the instance to the database
#         order.save()
#         # get the parent OD element of this ODD element
#         parent = element.getparent()
#         # get or create an instance of tblXmlOrders model that matches this parent OD's NO attribute 
#         xml_order, created = tblXmlOrders.objects.get_or_create(no=parent.get("NO"))
#         # set the invoicenumber field of the order instance to the xml_order instance
#         order.invoicenumber = xml_order
#         # save the order instance again to update the relationship
#         order.save()
#     # check if the element is a SP element
#     elif element.tag == "SP":
#         # get the PBC attribute of the SP element
#         pbc = element.get("PBC")
#         # create a new instance of the Barcode model with this attribute
#         barcode = Barcode(pbc=pbc)
#         # save the instance to the database
#         barcode.save()
#         # get the parent element of this SP element
#         parent = element.getparent()
#         # check if the parent element is an ODD element
#         if parent.tag == "ODD":
#         # get or create an instance of tblOrder model that matches this parent ODD's NO attribute 
#         order, created = tblOrder.objects.get_or_create(no=parent.get("NO"))
#         # set the tblorder field of the barcode instance to the order instance
#         barcode.tblorder = order
#         # save the barcode instance again to update the relationship
#         barcode.save()
#         # check if the parent element is another SP element
#         elif parent.tag == "SP":
#         # get or create an instance of Barcode model that matches this parent SP's PBC attribute 
#         parent_barcode, created = Barcode.objects.get_or_create(pbc=parent.get("PBC"))
#         # set the parent field of the barcode instance to the parent_barcode instance
#         barcode.parent = parent_barcode
#         # save the barcode instance again to update the relationship
#         barcode.save()
#     # check if the element is a TC element
#     elif element.tag == "TC":
#         # get the HC and BC attributes of the TC element
#         hc = element.get("HC")
#         bc = element.get("BC")
#         # create a new instance of the Barcode model with these attributes
#         barcode = Barcode(hc=hc, bc=bc)
#         # save the instance to the database
#         barcode.save()
#         # get the parent SP element of this TC element
#         parent = element.getparent()
#         # get or create an instance of Barcode model that matches this parent SP's PBC attribute 
#         parent_barcode, created = Barcode.objects.get_or_create(pbc=parent.get("PBC"))
#         # set the parent field of the barcode instance to the parent_barcode instance
#         barcode.parent = parent_barcode
#         # save the barcode instance again to update the relationship
#         barcode.save()
#         # loop over the child elements of the element
#         for child in element:
#          # call the function recursively on each child element
#          parse_element(child
                       
#                        #[
# # {"id":"452493","inspector":
# #     {"id":"452494","fname":"Leeann","lname":"Strong","mobile":"+92-9288-032-156","username":"erma.mcmillan2940@anyone.com","password":"friend"},
# #     "referraldate":"1995-09-23","company":
# #         {"id":"452495","name":"Mae Richie","nid":"46122682651",
# #          "address":"1250 Whitewater, Kaneohe, Georgia, 65340","phone":"+968-6649-885-125",
# #          "mobile":"+504-6767-942-487"}}]
