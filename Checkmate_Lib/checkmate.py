#import all site parser classes 

from parsers.kobo_parser import KoboSite
from parsers.livraria_parser import LivrariaSite
from parsers.google_books_parser import GoogleBooks
from parsers.test_book_store_parser import TestSite
from parsers.scribd_parser import ScribdSite
from parsers.audiobook_parser import AudioBookSite

"""
returns site parser.

params:
    slug: 2 character slug indicating the site
return:
    site: a BookSite object matching the passed slug.
"""
def get_book_site(slug_cased):
    site  = None
    slug = slug_cased.upper()
    if slug == GoogleBooks().site_slug:
        site = GoogleBooks()
    elif slug == KoboSite().site_slug:
        site = KoboSite() 
    elif slug == TestSite().site_slug:
        site = TestSite()
    elif slug == LivrariaSite().site_slug:
        site = LivrariaSite()  
    elif slug == ScribdSite().site_slug:
        site = ScribdSite()
    elif slug == AudioBookSite().site_slug:
        site = AudioBookSite()
    return site

   





