#import all site parser classes 

from kobo_parser import KoboSite
from livraria_parser import LivrariaSite
from PPP_D2D_Project.Checkmate_Lib.test_parser import TestSite




def get_book_site(slug_cased):
    site  = None
    slug = slug_cased.upper()
    if slug == 'GO':
        #Google Books
        pass
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

   





