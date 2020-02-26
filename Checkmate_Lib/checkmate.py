from kobo_parser import KoboSite

class BookSite:

    def __init__(self, BookSite):
        self.BookSite = BookSite
        pass

    #str -> SiteBookData
    #Given a direct link to a book page at a site,
    #parse it and return the SiteBookData of the info
    def get_book_data_from_site(self, url):

        sbd = SiteBookData()
        response = requests.get(url)
        content = response.content



        # We will add to this as we go
        sbd.book_title = titleParser(content)
        sbd.subtitle = subtitleParser(content)
        sbd.authors = authorsParser(content)
        sbd.isbn_13 = isbnParser(content)
        sbd.format =  formatParser(content)
        sbd.book_img = imageParser(content)
        sbd.book_img_url = imageUrlParser(content)
        sbd.description = descParser(content)
        sbd.series = seriesParser(content)
        sbd.volume_number = volumeParser(content)
        sbd.ready_for_sale = saleReadyParser(content)
        
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


def get_book_site(slug):
    site  = ""
    if slug == 'GO':
        #Google Books
        pass
    elif slug == 'KO':
        site = KoboSite() 
        return
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










