#import all site parser classes 

from parsers.kobo_parser import KoboSite
from parsers.livraria_parser import LivrariaSite
from parsers.google_books_parser import GoogleBooks
from parsers.test_parser import TestSite
from parsers.scribd_parser import ScribdSite


def get_book_site(slug_cased):
    site  = None
    slug = slug_cased.upper()
    if slug == 'GB':
        site = GoogleBooks()
    elif slug == 'KO':
        site = KoboSite() 
    elif slug == 'TB':
        site = TestSite()
    elif slug == 'LC':
        site = LivrariaSite()  
    elif slug == 'SC':
        site = ScribdSite()
        

    return site

   





