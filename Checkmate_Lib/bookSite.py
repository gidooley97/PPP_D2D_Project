import math, operator
from functools import reduce
from PIL import Image
import urllib.request


class BookSite:
    #str -> SiteBookData
    #Given a direct link to a book page at a site,
    #parse it and return the SiteBookData of the info
    def get_book_data_from_site(self, url):
        pass
        
        #str -> str
        #Given a book_id, return the direct url for the book
    def convert_book_id_to_url(self, book_id):
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





   
    