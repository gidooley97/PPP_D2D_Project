import math, operator
from functools import reduce
from PIL import Image
import urllib.request
from site_book_data import SiteBookData
import io
from lxml import etree
import requests
from io import BytesIO
import urllib.request
import mechanize
from abc import ABC, abstractmethod
import Levenshtein as lev


#BookSite is the parent class for all parsers, it does most of the default work for parsing, 
# you are able to override some functions and methods as needed.

#BookSite also contains the match_percentage functions that determines how good our search is. 

class BookSite(ABC):
    def __init__(self):
        self.match_list=[] #common to all sites
        self.site_slug=None
        self.search_url=None
    """
    Given  a url or html content  returns root.

    by default: receives urls, but also works for content.
    args:
        url:url to the html page
        content:html content of the page
    return:
        root:root of the html etree.
    """
    def get_root(self,url, content=None):
        if url is not None:
            content = requests.get(url).content#gets the book's page 
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        return tree.getroot()


    """
    str -> SiteBookData

    Given a direct link to a book page at a site,
    parse it and return the SiteBookData of the info.
    args:
        url: direct url to a book.
        content(optional): html content of page
    return:
        book_site_data: a SiteBookData object
    """
    def get_book_data_from_site(self, url, content=None):
        root = self.get_root(url,content) 
        title = self.title_parser(root)
        img_url = self.image_url_parser(root)
        img = self.image_parser(img_url)#use the img url to get image
        isbn13= self.isbn_parser(root)
        desc = self.desc_parser(root)
        frmt = self.format_parser(root)
        series = self.series_parser(root)
        vol_num = self.volume_parser(root)
        subtitle = self.subtitle_parser(root)
        authors = self.authors_parser(root)
        site_slug = self.site_slug
        if url:
            content = requests.get(url).content #html page content
        else:
            content = content
        url = url
        book_id = self.book_id_parser(url)
        parse_status =  self.get_parse_status(title,isbn13,desc,authors)
        ready_for_sale = self.sale_ready_parser(root) # figure out if 'pre-order' is considered ready for sale
        extra = self.extra_parser(root)
        book_site_data = SiteBookData(format=frmt, book_title=title, book_img= img, book_img_url=img_url, isbn_13=isbn13, description=desc, series=series, 
        volume=vol_num, subtitle=subtitle, authors=authors, book_id=book_id, site_slug=site_slug, parse_status=parse_status, url=url, content=content,
        ready_for_sale=ready_for_sale, extra=extra)
        
        return book_site_data
 

###############################################Utility Content Parser  Methods#########################################################################
    def title_parser(self, root):
        path = self.get_title_path()
        try:
            title_element = root.xpath(path)[0]
            title = title_element.text
        except:
            title = None# Fail
        return title

        
    def subtitle_parser(self,root):
        subtitle = None
        path = self.get_subtitle_path()
        try:
            if root.xpath(path):
                subtitle = root.xpath(path)[0].text
        except:
            subtitle = None# Fail
        return subtitle
            
    def authors_parser(self,root):

        path = self.get_authors_path()
        try: 
            author_elements = root.xpath(path)
            authors = []
            for auth_element in author_elements:
                authors.append(auth_element.text)
        except:
            authors = None #Fail
        return authors
    
    
    def book_id_parser(self, url):
        try:
            book_id  =url.split('/')[len(url.split('/'))-1] 
        except:
            book_id=None
        return book_id 
        

    def isbn_parser(self, root):
        path = self.get_isbn_path()
        try: 
            isbn_element = root.xpath(path)[0]
            isbn = isbn_element.text
        except:
            isbn = None
        return isbn

    def format_parser(self, root):
        path = self.get_format_path()
        try: 
            format = root.xpath(path)[0].text
        except:
            format = None
        return format_mapper(format)
   
    def format_mapper(self, format):
        if format is None:
            return None
        if "print" in format.lower() or 'hard' in format.lower():
             return "hard_cover"
        elif "audio" in format.lower():
            return "audio"
        else:
            return "ebook"

    def image_parser(self, url):
        image =None
        try:
            image = Image.open(urllib.request.urlopen(url))
        except:
            return None #Fail
        return image


    def image_url_parser(self, root):
        path = self.get_img_url_path()
        try:
            imageUrlParser_element = root.xpath(path)
            imageURL = imageUrlParser_element[0].text
        except:
            imageURL = None
        return imageURL
   
    def desc_parser(self, root):
        path = self.get_desc_path()
        try:
            desc_element = root.xpath(path)[0]
            desc = desc_element.text
        except:
            desc = None    
        return desc

    def series_parser(self, root):
        path = self.get_series_path()
        series_element = None
        series = None
        try:
            if root.xpath(path):
                series_element = root.xpath(path)[0] 
                series = series_element.text

            #Seperate series number from series title
            series_split = series.split('#')
        except:
            return None
        return series_split[0]

    
    def volume_parser(self, root):
    #method to be overriden if necessary. 
        return None


    # This is so different across parsers, we will leave this 
    # out of the master class
    def sale_ready_parser(self, root):
        xpath = self.get_sale_ready_path()
        try:
            sale_ready = root.xpath(xpath)[0]
        except:
            sale_ready= None
        return sale_ready

    def extra_parser(self, root):
        return {}
  
    def get_parse_status(self,title, isbn13, desc, authors):
         #determine parse_status checks if we have the most basic data about a book
        if title and isbn13 and desc and authors:
            return "FULLY PARSED"
        if title or isbn13 or desc or authors:
            return "PARTIALLY PARSED"
        return "UNSUCCESSFUL"

              
####################################### Get XPath Functions ######################################
    """
    Return specific xpath.

    These methods should be overriden. otherwise it won't work.
        params:
            None
        return:
            xpath-specific xpath(str) 
    """
    @abstractmethod
    def get_search_urls_after_search_path(self):
        return None

    @abstractmethod
    def get_title_path(self):
        return None
    
    @abstractmethod
    def get_subtitle_path(self):
        return None
    
    @abstractmethod
    def get_authors_path(self):
        return None

    @abstractmethod
    def get_isbn_path(self):
        return None
    @abstractmethod
    def get_format_path(self):
        return None

    @abstractmethod
    def get_img_url_path(self):
        return None

    @abstractmethod
    def get_desc_path(self):
        return None

    @abstractmethod
    def get_series_path(self):
        return None

    @abstractmethod
    def get_volume_path(self):
        return None

    @abstractmethod
    def get_sale_ready_path(self):
        return None
####################################################################################################################################
    """
    SiteBookData -> List[Tuple[SiteBookData, float]]
    
    Given a SiteBookData, search for the book at the `book_site` site and provide a list of 
    likely matches paired with how good of a match it is (1.0 is an exact match). 
    This should take into account all the info we have about a book, including the cover.
    Works for kobo and Test Book store. To be overriden by some site site.
    params:
        book_data: a  bookSiteData.
    returns:
        match:List[Tuple[SiteBookData, float]]
    """
    
    def find_book_matches_at_site(self, site_book_data, formats=None,pages=2):
        url =self.search_url
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open(url)  
        #selects the form to populate 
        br.select_form(class_="search-form")
        search_txt =None
        
        #populate the field. You may need to check if this is actually working
        if site_book_data.book_title:
            search_txt=site_book_data.book_title
        elif site_book_data.isbn_13:
            search_txt= site_book_data.isbn_13
        elif site_book_data.authors:
            search_txt = site_book_data.authors[0]
        if not search_txt:
            return []
        if self.site_slug=='KO':
            field_name= 'query'
        else:
            field_name ='s_bar'
        br[field_name] =search_txt
        self.match_list=[]
        #submit the form and get the returned page.
        res=br.submit()
        found = False
        page=1
        while page <=pages and not found:#limit the results we will get
            try:
                content =res.read()
                found=self.get_search_book_data_from_page(content, site_book_data, formats=formats)
                res=br.follow_link(text="Next")
                page+=1
            except mechanize._mechanize.LinkNotFoundError:#end of results
                break
        # print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        # print('formts', formats)
        self.filter_results_by_score(formats)
        return self.match_list

    """
    returns a list of tuple(score, book_data).

    Some parsers would need to override this method if necessary. For a single page of results, gets 
    urls and gets bookData from the the detail page of the book. 
    Works mainly for Kobo and TestBookStore.
    params:
        content: html content of a given page
        book_site_data_original:bookSiteData object. can be null if searching using attr.
       
    return: 
        None: 
    """
    def get_search_book_data_from_page(self, content,  book_site_data_original, formats=None):
        root = self.get_root(url=None, content=content)#force this method to work with content
        xpath = self.get_search_urls_after_search_path()
        #expects a path that will help us get the urls
        if  xpath is  None or root is None: 
            return False
        url_elements = root.xpath(xpath)
        if len(url_elements)==0 and formats:
            if super().get_book_data_from_site(url=None, content=content).format.lower() in ','.join(formats).lower():
                self.match_list.append(tuple([1.00,super().get_book_data_from_site(url=None, content=content)]))
                return True
            else:
                return False
        for url in url_elements:
            if self.site_slug == 'TB':
                url='http://127.0.0.1:8000'+url
            book_site_data_new= self.get_book_data_from_site(url)
            #book_site_data_new.print_all()
            score = self.match_percentage(book_site_data_original, book_site_data_new) 
            if score >=0.90 and book_site_data_new.format.lower() in formats:#Perfect match found
                # print('-------------------------------------')
                self.match_list=[]
                #book_site_data_new.print_all()
                book_data_score =tuple([score,book_site_data_new])
                self.match_list.append(book_data_score)
                return True
            book_data_score =tuple([score,book_site_data_new])
            self.match_list.append(book_data_score)
        return False


    """
    match_percentage takes 2 sitebookdata objects and compares them.  
    
    The function compares 8 attributes from each object against eachother.  
    We do not want to compare book_id,site_slug, url, or book_img_url since that changes from site to site
    This function also does not compare content, extra, or parse_status
    This function does not compare format since as of now all books are ebooks.
    !!!Update: Made sure to only count what is available inorder to have a better view of how similar the matches are.
    params:
        site_book1: first SiteBookData object
        site_book2: second SiteBookData object
    return:
        score:A float between 0 and 1.0 is returned to indicate the accuracy of the match.
    """
    def match_percentage(self,site_book1, site_book2):
        matching_points = 0 # Keeps track of matching attributes
        total =0
        if site_book1.book_title and site_book2.book_title:
            matching_points += lev.ratio(site_book1.book_title.strip().lower(), site_book2.book_title.strip().lower())*200
            total += 200

        if site_book1.isbn_13 and site_book2.isbn_13:
            matching_points += lev.ratio(site_book1.isbn_13.strip().lower(),site_book2.isbn_13.strip().lower())*750
            total += 750
        
        if site_book1.description and site_book2.description:
            matching_points += lev.ratio(site_book1.description.strip().lower(),site_book2.description.strip().lower())* 5
            total += 5
        
        if site_book1.series and site_book2.series:
            matching_points += lev.ratio(site_book1.series.strip().lower(), site_book2.series.strip().lower())*5
            total += 5

        if site_book1.volume and site_book2.volume:
            matching_points += lev.ratio(site_book1.volume.strip().lower(),site_book2.volume.strip().lower())*5
            total += 5
        
        if site_book1.subtitle and site_book2.subtitle:
            matching_points += lev.ratio(site_book1.subtitle.lower(), site_book2.subtitle.lower())*5
            total += 5

        # Compare author lists
        if site_book1.authors and site_book2.authors:
            matching_points += self.compare_authors(site_book1.authors, site_book2.authors)*20
            total += 20
            
        if site_book1.ready_for_sale and site_book2.ready_for_sale and site_book1.ready_for_sale.strip().lower() == site_book2.ready_for_sale.strip().lower():
            matching_points += lev.ratio(site_book1.ready_for_sale.strip().lower(), site_book2.ready_for_sale.strip().lower())*5
            total += 5

        # Allows a small margin of difference
        if site_book1.book_img_url and   site_book2.book_img_url:
            if self.book_img_matcher(site_book1, site_book2) <= 10:
                matching_points += 5
            total += 5
        if total ==0:
            return 0
        return matching_points/total

    """
    Compares the authors in SiteBookData 1 and SiteBookData2 objects

    Params:
        auth1: the list of authors in site_book_data1
        auth2: the list of authors in site_book_data2
    return:
        cumulative levenshtein ratio.
    """
    def compare_authors(self,auth1, auth2):
        auth_str1 =  ','.join(auth1)
        auth_str2 = ','.join(auth2)
        #print("score",lev.ratio(auth_str1, auth_str2) )
        return lev.ratio(auth_str1, auth_str2)

    """
    loops over the match(List(tuple(score, bookSiteData))) list and 
    
    filters out matches with score less than 20%.
    params:
        None
    return:
        None
    """
    def filter_results_by_score(self, formats):
        if not formats:
            return  []
        myList=list(filter(lambda x: x[0]>=0.7 and x[1].parse_status== "FULLY PARSED" and x[1].format.lower() in ','.join(formats).lower(),self.match_list))
        self.match_list=myList
        self.match_list.sort(key = lambda x: x[0],reverse=True)
        
    """
    Utility function for image comparison. 

    https://snipplr.com/view/757/compare-two-pil-images-in-python Referenced
    params:
        sitebook1:SiteBookData object
        sitebook2:SiteBookData object
    return:
        rms:returns the root-mean square difference between the 2 provided images. 0 is an exact match
    """
    def book_img_matcher(self,sitebook1, sitebook2):
        try: # catch exceptions
            image1 = Image.open(urllib.request.urlopen(sitebook1.book_img_url)).histogram()
            image2 = Image.open(urllib.request.urlopen(sitebook2.book_img_url)).histogram()
        except:
            return 11 # to indicate total misamtch
 
        rms = math.sqrt(reduce(operator.add,
	    map(lambda a,b: (a-b)**2, image1, image2))/len(image1)) 
        return rms

    """
    Given a book_id, return the direct url for the book.

    To be overriden by all sites.
    params:
        book_id: the book unique identifier.
    return:
        url:direct url to the book. 
    """
    @abstractmethod
    def convert_book_id_to_url(self, book_id):
        return None








   
    