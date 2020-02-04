# put process onix code  goes here
from lxml import etree
path= "real_stuff_onix3_01.xml"
ns = {"d":"http://ns.editeur.org/onix/3.0/reference"}


SALE_FLAGS_REF = {"00":"Unspecified", "01":"Cancelled", "02":"Forthcoming","03":"Postponed indefinitely","04":"Active","05":"No longer our product",
"06":"Out of stock indefinitely","07":"Out of print","08":"Inactive","09":"Unknown","10":"Remaindered",
"11":"Withdrawn from sale","12":"Recalled","13":"Active, but not solved separately","15":"Recalled","16":"Temporarily withdrawn from sale","17":"Permanently withdraw from sale"}
def load_onix_file(path):
    try:
        context = etree.parse(path)
    except:
        print("unable to parse onix file.")
        raise
    return context    


def process_data():
    root = load_onix_file(path)
    product_elemnts = root.xpath("d:Product", namespaces=ns)
    for prod_el in product_elemnts[:10]: 
        #print("H")
        isbn_13 = prod_el.xpath("d:ProductIdentifier[d:ProductIDType=15]/d:IDValue", namespaces=ns)[0].text
        auth_els = prod_el.xpath(".//d:Contributor[d:ContributorRole='A01']/d:PersonName", namespaces=ns)
        authors=[]
        for auth in auth_els:
            authors.append(auth.text)
            
        # lang_el = prod_el.xpath(".//d:Language[d:LanguageRole='01']/d:LanguageCode", namespaces=ns)
        # language = lang_el[0].text
        #title_el = prod_el.xpath(".//d:TitleDetail[d:TitleType='01']/d:PersonName", namespaces=ns)
        #let's talk about series and title
        desc_el = prod_el.xpath(".//d:TextContent[d:TextType='03']/d:Text", namespaces=ns)[0].text

        publ_status_el= prod_el.xpath(".//d:PublishingStatus", namespaces=ns)[0].text
        
        price = prod_el.xpath(".//d:Price[d:PriceType='01']/d:PriceAmount", namespaces=ns)[0].text
        
        
        #print(price)

        #logic to check if we need to do an insert.
        
process_data()





