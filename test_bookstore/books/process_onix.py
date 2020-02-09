# put process onix code  goes here

from lxml import etree

ns = {"d": "http://ns.editeur.org/onix/3.0/reference"}


class BookData:
    def __init__(self, title, auth, isbn_13, subtitle, series, volume, desc, book_format, sale_flag):
        self.title = title
        self.authors = auth
        self.isbn_13 = isbn_13
        self.subtitle = subtitle
        self.series = series
        self.volume = volume
        self.desc = desc
        self.book_formats = book_format
        self.sale_flag = sale_flag
    def __str__(self):
        return self.title +' '+self.isbn_13

def test():
    bookdata = BookData('some title', 'Blaise Mahoro','12321313112334', 'df', 'df', 'df', 'df', 'df', 'df')
    #book = Book.objects.create( title='Tiele', authors = 'ldsfklsdfns fsdfn, adfsjdf. dfs',isbn_13= '',subtitle ='',series='',volume='',desc='',book_formats='',sale_flag = '')
    return bookdata

PUBLISHING_STATUS = {"00": "Unspecified", "01": "Cancelled", "02": "Forthcoming", "03": "Postponed indefinitely", "04": "Active", "05": "No longer our product",
                  "06": "Out of stock indefinitely", "07": "Out of print", "08": "Inactive", "09": "Unknown", "10": "Remaindered",
                  "11": "Withdrawn from sale", "12": "Recalled", "13": "Active, but not solved separately", "15": "Recalled", "16": "Temporarily withdrawn from sale", "17": "Permanently withdraw from sale"}

BOOK_FORMATS={"00":"Undefined","AA":"Audio","AB":"Audio cassette","AC":"CD-Audio","AD":"DAT",
 "AE":"Audio disc","AF":"Audio tape","AG":"MiniDisc", "AH":"CD-Extra","AI":"DVD Audio","AJ":"Downloadable audio file",
 "AK":"Pre-recorded digital audio player","BA":"Book","BB":"Hardback","BC":"Paperback / softback",
  "VL":"VCD","VM":"SVCD", 	"VN":"HD DVD","VO": "Blu-ray", "EA":"Digital (delivered electronically)",
   "EB":"Digital download and online","EC":"Digital online","ED":"Digital download"}	 	
		 	

def load_onix_file(path):
    
    try:
        context = etree.parse(path)
    except:
        print("unable to parse onix file.")
        raise
    return context


def process_data(root):
    #path= "real_stuff_onix3_01.xml"
    #root = load_onix_file(path)
    book_list = []

    product_elemnts = root.xpath("d:Product", namespaces=ns)
    for prod_el in product_elemnts:
        isbn_13 = prod_el.xpath(".//d:ProductIdentifier[d:ProductIDType='15']/d:IDValue", namespaces=ns)[0].text

        auth_els = prod_el.xpath(".//d:Contributor[d:ContributorRole='A01']/d:PersonName", namespaces=ns)
        authors = []
        for auth in auth_els:
            authors.append(auth.text)

        # lang_el = prod_el.xpath(".//d:Language[d:LanguageRole='01']/d:LanguageCode", namespaces=ns)
        # language = lang_el[0].text
        title = prod_el.xpath(".//d:DescriptiveDetail/d:TitleDetail[d:TitleType='01']/d:TitleElement/d:TitleText", namespaces=ns)[0].text
        #let's talk about series and title
        subtitle=''
        if prod_el.xpath(".//d:DescriptiveDetail/d:TitleDetail[d:TitleType='01']/d:TitleElement/d:Subtitle", namespaces=ns):
            subtitle=prod_el.xpath(".//d:DescriptiveDetail/d:TitleDetail[d:TitleType='01']/d:TitleElement/d:Subtitle", namespaces=ns)[0].text
        collection_el=prod_el.xpath(".//d:Collection", namespaces=ns)
        volume = ''
        if collection_el:
            if prod_el.xpath(".//d:PartNumber", namespaces=ns):
                volume = prod_el.xpath(".//d:PartNumber", namespaces=ns)[0].text
        description = prod_el.xpath(".//d:TextContent[d:TextType='03']/d:Text", namespaces=ns)[0].text
        pub_stat_code=prod_el.xpath(".//d:PublishingStatus", namespaces=ns)[0].text
        publ_status =PUBLISHING_STATUS[pub_stat_code]
        book_format_code =  prod_el.xpath(".//d:ProductForm", namespaces=ns)[0].text
        book_format=BOOK_FORMATS[book_format_code]
        sale_flag= (pub_stat_code=="13" or pub_stat_code=="04")
        #data
        auths= ','.join(authors)
        series =''
        
        tmp_book_data = BookData(title,auths,isbn_13,subtitle,series,volume ,description, book_format,sale_flag)
        book_list.append(tmp_book_data) #Add book data to list
    return book_list


#process_data()