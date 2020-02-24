
def get_book_site(slug):

    if slug == 'GO':
        #Google Books
        pass
    elif slug == 'KO':
        #Kobo
        pass
    elif slug == 'TB':
        #Test Bookstore
        pass
    elif slug == 'LC':
        #Livraria Clutura
        pass
    elif slug == 'SC':
        #Scribd
        pass

class book_site:

    def __init__(self, BookSite):
        self.BookSite = BookSite
        pass

    def get_book_data_from_site(self, data):
        #str -> SiteBookData
        #Given a direct link to a book page at a site,
        #parse it and return the SiteBookData of the info
        pass

    def find_book_matches_at_site(self, book_data):
        #SiteBookData -> List[Tuple[SiteBookData, float]]
        #Given a SiteBookData, search for the book at the `book_site` site and provide a list of 
        #likely matches paired with how good of a match it is (1.0 is an exact match). 
        # This should take into account all the info we have about a book, including the cover."""
        pass

    def covert_book_id_to_url(self, book_id):
        #str -> str
        #Given a book_id, return the direct url for the book
        pass