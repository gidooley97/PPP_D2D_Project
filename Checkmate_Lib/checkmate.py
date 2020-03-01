from site_book_data import SiteBookData
import io
from lxml import etree
from PIL import Image
from io import BytesIO
import urllib.request
import io
import mechanize
import requests
import math, operator
from functools import reduce



class BookSite:

    #str -> SiteBookData
    #Given a direct link to a book page at a site,
    #parse it and return the SiteBookData of the info
    def get_book_data_from_site(self, url):
        sbd = SiteBookData()
        response = requests.get(url)
        content = response.content



        # We will add to this as we go
        sbd.book_title = self.titleParser(content)
        sbd.subtitle = self.subtitleParser(content)
        sbd.authors = self.authorsParser(content)
        sbd.isbn_13 = self.isbnParser(content)
        sbd.format =  self.formatParser(content)
        sbd.book_img = self.imageParser(content)
        sbd.book_img_url = self.imageUrlParser(content)
        sbd.description = self.descParser(content)
        sbd.series = self.seriesParser(content)
        sbd.volume_number = self.volumeParser(content)
        sbd.ready_for_sale = self.saleReadyParser(content)
        
        return sbd


        #str -> str
        #Given a book_id, return the direct url for the book
    def covert_book_id_to_url(self, book_id):
        pass

        #------------ Utility Methods -------------
    def titleParser(self, content):
        pass

    def subtitleParser(self,content):
        pass
            
    def authorsParser(self,content):
        pass

    def isbnParser(self, content):
        pass

    def formatParser(self, content):
        pass

    def imageParser(self, content):
        pass

    def imageUrlParser(self, content):
        pass

    def descParser(self, content):
        pass

    def seriesParser(self, content):
        pass

    def volumeParser(self, content):
        pass

    def saleReadyParser(self, content):
        pass

    def extraParser(self, content):
        pass
  





    #SiteBookData -> List[Tuple[SiteBookData, float]]
    #Given a SiteBookData, search for the book at the `book_site` site and provide a list of 
    #likely matches paired with how good of a match it is (1.0 is an exact match). 
    # This should take into account all the info we have about a book, including the cover."""
        def find_book_matches_at_site(self, book_data):
            pass


##################### End of Class ##############################


def get_book_site(slug_cased):
    site  = ""
    slug = slug_cased.upper()
    if slug == 'GO':
        #Google Books
        pass
    elif slug == 'KO':
        site = KoboSite() 
    elif slug == 'TB':
        #Test Bookstore
        pass
    elif slug == 'LC':
        #Livraria Clutura
        pass
    elif slug == 'SC':
        #Scribd
        pass

    return site

    # Returns the root-mean square difference between the 2 provided images. 0 is an exact match
    # https://snipplr.com/view/757/compare-two-pil-images-in-python Referenced
def book_img_matcher(sitebook1, sitebook2):
    #h1 = Image.open(sitebook1.book_img_url).histogram()
    #h2 = Image.open(sitebook2.book_img_url).histogram()
    image1 = Image.open(urllib.request.urlopen(sitebook1.book_img_url)).histogram()
    image2 = Image.open(urllib.request.urlopen(sitebook2.book_img_url)).histogram()
 
    rms = math.sqrt(reduce(operator.add,
	map(lambda a,b: (a-b)**2, image1, image2))/len(image1)) 
    return rms





   
 # match_percentage tkes 2 sitebookdata objects
# and compares them.  The function compares 8 
# attributes from each object against eachother.  
# A float between 0 and 1.0 is returned to indicate 
# the accuracy of the match.
# Each attribute is given a weight to indicate it's importance
# to the match percentage.
# We do not want to compare book_id,site_slug, url, or book_img_url since that changes from site to site
# This function also does not compare content, extra, or parse_status
# This function does not compare format since as of now all books are ebooks

def match_percentage(site_book1, site_book2):
    matching_points = 0 # Keeps track of matching attributes

    if(site_book1.book_title == site_book2.book_title):
        matching_points += 200

    if(site_book1.isbn_13 == site_book2.isbn_13):
        matching_points += 750
        
    if(site_book1.description == site_book2.description):
        matching_points += 5
        
    if(site_book1.series== site_book2.series):
        matching_points += 5
        
    if(site_book1.volume == site_book2.volume):
        matching_points += 5
        
    if(site_book1.subtitle == site_book2.subtitle):
        matching_points += 5

        # Compare author lists
    if set(site_book1.authors) == set(site_book2.authors):
        matching_points += 20

            
    if(site_book1.ready_for_sale == site_book2.ready_for_sale):
        matching_points += 5

     # Allows a small margin of difference
    if book_img_matcher(site_book1, site_book2) <= 10:
        matching_points += 5
   


    return matching_points/1000

   


######################################################################
######################################################################
######################################################################
########################## KoboSite ##################################
######################################################################
######################################################################
######################################################################




############ KoboSite Class ################
"""parses the book data from kobo"""
class KoboSite:
    
    def __init__(self):
        self.site_slug = "KB"
        self.search_url="https://www.kobo.com/"
        self.url_to_book_detail ="https://www.kobo.com/us/en/ebook/"#set to ebook bcs D2D deals with ebooks mainly
        self.match_list=[]
    #returns list of site books
    def get_book_data_from_site(self,url):
        content = fetch(url) #gets the book's page 
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot() 
        title = self.titleParser(root)
        img_url = self.imageUrlParser(root)
        img = self.imageParser(img_url)#use the img url to get image
        isbn13= self.isbnParser(root)
        desc = self.descParser(root)
        frmt = self.formatParser(root)
        series = self.seriesParser(root)
        vol_num = self.volumeParser(root)
        subtitle = self.subtitleParser(root)
        authors = self.authorsParser(root)
        site_slug = self.site_slug
        content =content #html page content
        url = url
        book_id = self.book_id_parser(url)
        parse_status =  self.get_parse_status(title,isbn13,desc,authors)
        ready_for_sale = self.saleReadyParser(root) # figure out if 'pre-order' is considered ready for sale
        extra = self.extraParser(root)
        book_site_data = SiteBookData(frmt, title, img, img_url,isbn13,desc, series, 
        vol_num, subtitle, authors,book_id, site_slug, parse_status, url, content,
        ready_for_sale, extra)
        return book_site_data

        

    def find_matches_at_site(self,site_book_data):
        url =self.search_url
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open(url)  
        #selects the form to populate 
        br.select_form(class_="search-form")
        search_txt =''
        #populate the field. You may need to check if this is actually working
        if site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.isbn13:
            search_txt= site_book_data.isbn_13
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        if not search_txt:
            return []
        br['query'] =search_txt
        
        #submit the form and get the returned page.
        res=br.submit()
        self.get_book_data_from_page(res.read(), site_book_data)
        return self.match_list # for testing I get the first page
        while(True):
            try:
                print("nextpage")
                res=br.follow_link(text="Next")
                self.get_book_data_from_page(res.read(), site_book_data)
            except mechanize._mechanize.LinkNotFoundError:
                print("Reached end of results")
                return self.match_list
                break
            
    #gets url and pass it to get_book_data_from_site to get books
    def get_book_data_from_page(self, content, book_site_dat_1):
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        url_elements = root.xpath(".//p[@class='title product-field']/a/@href")

        for url in url_elements:
            #call function to get book data with url
            book_site_dat_tmp= self.get_book_data_from_site(url)
            score = self.match_percentage(book_site_dat_1, book_site_dat_tmp) 
            book_data_score =tuple([score,book_site_dat_tmp])
            #print('score', score)
            #book_site_dat_tmp.print_all()
            self.match_list.append(book_data_score)
        
                   

    # Merge branches
    # convert id to url
    # if statement to determine what attribute to search with
    # fill form with site_book_data
    # Go through search page results and visit urls while "clicking" 
    # next button (this may be site specific function)
    # get_book_data from urls and run through matching 
    # function and add bookdata and score to dictionary
    # Order dictionary by score (high to low)
    # Return dictionary

    # return url
    def convert_book_id_to_url(self,book_id):
        return self.url_to_book_detail+book_id

    #------------ Utility Methods -------------







    


    def titleParser(self, root):
        title_element = root.xpath(".//h1/span[@class='title product-field']")[0]
        title = title_element.text
        return title

    def subtitleParser(self,root):
        subtitle = ''
        if root.xpath(".//h2/span[@class='subtitle product-field']"):
            subtitle = root.xpath(".//h2/span[@class='subtitle product-field']")[0].text
        return subtitle
        
        

    def authorsParser(self,root):
        author_elements = root.xpath("//span[@class='visible-contributors']/a[@class='contributor-name']")
        authors = []
        for auth_element in author_elements:
            authors.append(auth_element.text)
        return authors

    def isbnParser(self, root):
        isbn_elements = root.xpath("//div[@class='bookitem-secondary-metadata']/ul/li")
        isbn=''
        for isbn_tmp in isbn_elements:
            if isbn_tmp.text.strip()=='ISBN:':
                isbn =isbn_tmp.xpath('./span')[0].text
        return isbn

    def book_id_parser(self, url):
        #book_id is the last part of the url
        book_id  =url.split('/')[len(url.split('/'))-1] 
        return book_id 
        
    def formatParser(self, root):
        #Kobo only has ebooks and audio books
        format_element = root.xpath("//div[@class='bookitem-secondary-metadata']/h2")[0]
        form = format_element.text.strip().split(' ')[0]
        return form
        
    def imageParser(self, url):
        #response = requests.get(url)
        image = Image.open(urllib.request.urlopen(url))
        image.save("here.jpg")
        return image


    def imageUrlParser(self, root): 
        imgUrl_element = root.xpath("//img[@class='cover-image  notranslate_alt']/@src")[0] 
        imgUrl = "http:" + imgUrl_element
        return imgUrl

    def descParser(self, root):
        desc_string = ""
        desc_element_list = root.xpath("//div[@class='synopsis-description']")[0]
        print(len(desc_element_list))
        for element in desc_element_list:
            if(element.xpath("//p")):
                if(isinstance(element.text,str)):
                    desc_string += element.text

        return desc_string

    def seriesParser(self, root):
        series_element = ''
        series = ''
        if root.xpath(".//span[@class='product-sequence-field']/a"):
            series_element = root.xpath(".//span[@class='product-sequence-field']/a")[0] 
            series = series_element.text

 #for element in desc_element.xpath("//p"):
        #desc_string += element.text


        #Seperate series number from series title
        series_split = series.split('#')
        return series_split[0]

    def get_parse_status(self,title, isbn13, desc, authors):
         #determine parse_status checks if we have the most basic data about a book
        if title and isbn13 and desc and authors:
            return "UNSUCCESSFUL"
        return "FULLY_PARSED"


    def volumeParser(self, root):
        series_element = ''
        volume = ''
        if root.xpath(".//span[@class='product-sequence-field']/a"):
            series_element = root.xpath(".//span[@class='product-sequence-field']/a")[0] 
            series = series_element.text
        
            #Seperate series number from series title
            
            series_split = series.split('#')
            if len(series_split) > 1:
                volume = series_split[1]
        return volume

  
    def saleReadyParser(self, root):
        desc= root.xpath("//h2[@class='pricing-title']")[0].text
        sale_flag = 0 # 0 = Buy   1 = Pre-order
        status = ""
        # Check for the words 'Buy' and 'Pre-Order
        desc_list = desc.split(' ')
        for word in desc_list:
            if word == 'Buy':
                sale_flag = 0
                status = "Buy Now"
            if word == 'Pre-Order':
                sale_flag = 1
                status = "Pre-order"

        return status


    def extraParser(self, root):
        return {}




    #parseAll parses all data, prints it, and 
    #stores it in a SiteBookData Object
    def parseAll(self, site, content):
        
        print("Title: ")
        site.titleParser(content)
        print("Authors: ")
        site.authorsParser(content)
        print("ISBN: ")
        site.isbnParser(content)
        print("Format: ")
        site.formatParser(content)
        print("Description: ")
        site.descParser(content)
        print("Subtitle: ")
        site.subtitleParser(content)
        print("Series: ")
        site.seriesParser(content)
        print("Volume: ")
        site.volumeParser(content)
        print("Image URL: ")
        site.imageUrlParser(content)
        print("Ready Status: ")
        site.saleReadyParser(content)
        print("Image Saved")
        site.imageParser(content)


   
   
    ############# End of Class #################



def main():

    site = KoboSite() 
    url="https://www.kobo.com/us/en/ebook/c-c-2"
    book_site_data = site.get_book_data_from_site(url)
    book_site_data.print_all()
    myList = site.find_matches_at_site(book_site_data)
    #Go throigh all the matches printing score and bookSiteData.
    for book in myList:
        print(str(book[0])+" \n")
        book[1].print_all()
  
def fetch(url):
    response = requests.get(url)
    #print(response.content)
    return response.content


























