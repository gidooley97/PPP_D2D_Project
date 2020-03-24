import math, operator
from functools import reduce
from PIL import Image
import urllib.request
from site_book_data import SiteBookData
import io
from lxml import etree
import requests
from PIL import Image
import requests
from io import BytesIO
import urllib.request
from bookSite import BookSite
import mechanize
from bs4 import BeautifulSoup


class BookSite:

    # Given a URL, this function returns a root node
    def get_root(self,url):
        content = requests.get(url).content#gets the book's page 
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()


    #str -> SiteBookData
    #Given a direct link to a book page at a site,
    #parse it and return the SiteBookData of the info
    def get_book_data_from_site(self, url):
       get_root(url)
        


        #str -> str
        #Given a book_id, return the direct url for the book
        # This will most likely have to be left blank
    def convert_book_id_to_url(self, book_id):
        pass

        #------------ Utility Methods -------------
    def titleParser(self, root):
        path = self.get_title_path()
        try:
            title_element = root.xpath("path")[0]
            title = title_element.text
    except:
        title = "F" # Fail
        return title

        
        

    def subtitleParser(self,root):
        subtitle = ''
        path = self.get_subtitle_path()
        try:
            if root.xpath(path):
                subtitle = root.xpath(path)[0].text
        except:
            subtitle = "F" # Fail
        return subtitle
            
    def authorsParser(self,root):

        path = self.get_authors_path()
        try: 
            author_elements = root.xpath(path)
            authors = []
            for auth_element in author_elements:
                authors.append(auth_element.text)
        except:
            authors = "F" #Fail
        return authors

    def isbnParser(self, root):
        path = self.get_isbn_path()
        try: 
            isbn_element = root.xpath(path)[0]
            isbn = format_element.text
        except:
            isbn = 'F'
        return isbn

    def formatParser(self, root):
        path = self.get_format_path()
        try: 
            format_element = root.xpath(path)[0]
            format = format_element.text.strip().split(' ')[0]
        except:
            format = 'F'
        return format

    def imageParser(self, url):
        #response = requests.get(url)
        image =None
        try:
            image = Image.open(urllib.request.urlopen(url))
        except:
            return 'F' #Fail
        return image


    def imageUrlParser(self, root):
        path = self.get_img_url_path()
        try:
            imgUrl_element = root.xpath(path)[0] 
            imgUrl = "http:" + imgUrl_element
        except:
            imgUrl = 'F'
        return imgUrl

    def descParser(self, root):
        path = self.get_desc_path()
        try:
            desc_element_list = root.xpath(path)[0]
            # need to decide whther to take all or only the 1st p tag content
            xmlstr = etree.tostring(desc_element_list, encoding='utf8', method='xml')  
            desc = BeautifulSoup(xmlstr,features="lxml") 
        except:
            desc = 'F'    
        return desc.get_text()

    def seriesParser(self, root):
        path = self.get_series_path()
        series_element = ''
        series = ''
        try:
            if root.xpath(path):
                series_element = root.xpath(path)[0] 
                series = series_element.text

            #Seperate series number from series title
            series_split = series.split('#')
        except:
            return 'F'
        return series_split[0]

    def volumeParser(self, root):
        path = get_volume_path()
        series_element = ''
        volume = ''
        try:

            if root.xpath(path):
                series_element = root.xpath(path)[0] 
                series = series_element.text
            
                #Seperate series number from series title
                
                series_split = series.split('#')
                if len(series_split) > 1:
                    volume = series_split[1]
        except:
            volume = 'F'
        return volume


    # This is so different across parsers, we will leave this 
    # out of the master class
    def saleReadyParser(self, root):
        pass

    def extraParser(self, root):
        pass
  
    def get_parse_status(self,title, isbn13, desc, authors):
         #determine parse_status checks if we have the most basic data about a book
        if title and isbn13 and desc and authors:
            return "UNSUCCESSFUL"
        return "FULLY_PARSED"
    ########################## Get Path Functions ##########################
    def get_title_path():
        pass
    
    def get_subtitle_path():
        pass
    
    def get_authors_path():
        pass

    def get_isbn_path():
        pass

    def get_format_path():
        pass

    def get_img_url_path():
        pass

    def get_desc_path():
        pass

    def get_series_path():
        pass

    def get_volume_path():
        pass
    

    #SiteBookData -> List[Tuple[SiteBookData, float]]
    #Given a SiteBookData, search for the book at the `book_site` site and provide a list of 
    #likely matches paired with how good of a match it is (1.0 is an exact match). 
    # This should take into account all the info we have about a book, including the cover."""
    def find_book_matches_at_site(self, book_data):
            pass

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

    def match_percentage(self,site_book1, site_book2):
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

   
    #Utility function for image comparison
    # Returns the root-mean square difference between the 2 provided images. 0 is an exact match
    # https://snipplr.com/view/757/compare-two-pil-images-in-python Referenced
def book_img_matcher(sitebook1, sitebook2):
    #h1 = Image.open(sitebook1.book_img_url).histogram()
    #h2 = Image.open(sitebook2.book_img_url).histogram()
    try: # catch exceptions
        image1 = Image.open(urllib.request.urlopen(sitebook1.book_img_url)).histogram()
        image2 = Image.open(urllib.request.urlopen(sitebook2.book_img_url)).histogram()
    except:
        return 11 # to indicate total misamtch
 
    rms = math.sqrt(reduce(operator.add,
	map(lambda a,b: (a-b)**2, image1, image2))/len(image1)) 
    return rms





   
    