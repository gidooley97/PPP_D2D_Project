

import os
import sys
from pathlib import Path
from  builtins import any as b_any
from concurrent.futures import ThreadPoolExecutor

#a hacky way of getting around the problem of importing modules.
root= str(Path(__file__).resolve().parents[2])
dir_of_interest = root+'/Checkmate_Lib'
modules = {}
sys.path.append(dir_of_interest)
for module in os.listdir(dir_of_interest):
    if '.py' in module and '.pyc' not in module:
        current = module.replace('.py', '')
        modules[current] = __import__(current)

get_book_site = modules['checkmate'].get_book_site
SiteBookData = modules['site_book_data'].SiteBookData



"""
Process the request to search using CheckMate Library. 

Params:
    -permissions: permission codenames granted to the user.
    -query: parameters sent by the user.
return:
    -list: list of matches found from every site that the user
     has permission to search with.
"""
def  process(permissions, query):
    return search(permissions,query)    


"""
Search the request to search using CheckMate Library. 

Params:
    -permissions: permission codenames granted to the user.
    -query: parameters sent by the user.
return:
    -list: list of matches found from every site that the user
     has permission to search with.
"""
def search(permissions, query):
    book_title=query.get('title')
    if query.get('authors'):
        authors = str(query.get('authors')).split(',')
    else:
        authors =None
    isbn_13 = query.get('isbn')
    book_url = query.get('book_url')
    matches = []
    #remember to handle json 
    
    if b_any('scribd' in x for x in permissions):
        matches.extend(get_matches('SC',book_title,authors,isbn_13,book_url))        

    if b_any('google' in x.lower() for x in permissions):
        matches.extend(get_matches('GB',book_title,authors,isbn_13,book_url))

    if b_any('kobo' in x.lower() for x in permissions):
        matches.extend(get_matches('KO',book_title,authors,isbn_13,book_url))        

    if b_any('test' in x.lower() for x in permissions):
        matches.extend(get_matches('TB',book_title,authors,isbn_13,book_url)) 

    if b_any('livraria' in x.lower() for x in permissions):
        matches.extend(get_matches('LC',book_title,authors,isbn_13,book_url))        

    if b_any('audio' in x.lower() for x in permissions):
        matches.extend(get_matches('AU',book_title,authors,isbn_13,book_url))
    
    return matches
    
"""
Get book matches from a specified site.

Params:
    -site_slug:site slug
    -book_title
    -authors: list of authors
    -isbn_13
    -book_url
return:
    -matches: list of site_book_data objects.
"""
    
def get_matches(site_slug, book_title, authors,isbn_13, book_url):
    book_site = get_book_site(site_slug)
    if book_url:
        site_book_data =book_site.get_book_data_from_site(book_url)
    else:
        site_book_data = SiteBookData(book_title=book_title, authors=authors,
                            isbn_13=isbn_13)

    matches =  book_site.find_book_matches_at_site(site_book_data)
    return list(map(lambda x:x[1],matches))

