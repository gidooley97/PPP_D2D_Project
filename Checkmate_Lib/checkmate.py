#import all site parser classes 

from kobo_parser import KoboSite
from livraria_parser import LivrariaSite
from google_books_parser import GoogleBooks
from test_parser import TestSite


def get_book_site(slug_cased):
    site  = None
    slug = slug_cased.upper()
    if slug == 'GO':
        site = GoogleBooks()
    elif slug == 'KO':
        site = KoboSite() 
    elif slug == 'TB':
        site = TestSite()
    elif slug == 'LC':
        site = LivrariaSite()  
    elif slug == 'SC':
        #Scribd
        pass

    return site

   





