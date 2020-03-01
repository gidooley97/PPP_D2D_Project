#import all site parser classes 

from kobo_parser import KoboSite




def get_book_site(slug_cased):
    site  = None
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

   





