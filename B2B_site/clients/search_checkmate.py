

import os
import sys
from pathlib import Path
from  builtins import any as b_any
from concurrent.futures import ThreadPoolExecutor


# getting around the problem of importing modules.
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
def  process(sites_allowed, formats, query=0, data=0):
    if data:#json
        params = data
    else:#attribut fields
        params = query
    return search(sites_allowed,formats,params)    


"""
Search the request to search using CheckMate Library. 

Params:
    -sites_allwed : sites the user has accewss to search.
    -query: parameters sent by the user.
return:
    -list: list of matches found from every site that the user
     has permission to search with.
"""
def search(sites_allowed, formats, query):
    matches = []
    book_title=query.get('title')
    if query.get('authors'):
        authors = str(query.get('authors')).split(',')
    else:
        authors =None
    isbn_13 = query.get('isbn')

    if book_title is None and authors is None and isbn_13 is None:
        return [] 

    all_site_slugs = get_sites(sites_allowed)

    for site_slug in all_site_slugs:
        matches.extend(get_matches(site_slug,book_title,authors,isbn_13, formats))
        
    return matches
    
"""
Get book matches from a specified site.

Params:
    -site_slug:site slug
    -book_title
    -authors: list of authors
    -isbn_13

return:
    -matches: list of site_book_data objects.
"""
    
def get_matches(site_slug, book_title, authors,isbn_13, formats):
    try:
        book_site = get_book_site(site_slug)
     
        site_book_data = SiteBookData(book_title=book_title, authors=authors,
                            isbn_13=isbn_13)

        matches =  book_site.find_book_matches_at_site(site_book_data)
        # for book in matches:
        #         print("=======================================================================================")
        #         print("Score    : ", str(book[0]))
        #         book[1].print_all()
        return list(map(lambda x:x[1],matches))
    except:
        return []


"""
Gets site_slugs that the user has permission to access.

Params:
    -permissions: sites allowed to be searched by user
Returns:
    site_slugs: list of site slugs
"""
def get_sites(permissions):
    site_slugs =[]
    if b_any('scribd' in x for x in permissions):
        site_slugs.append('SC')        

    if b_any('google' in x.lower() for x in permissions):
        site_slugs.append('GB') 

    if b_any('kobo' in x.lower() for x in permissions):
        site_slugs.append('KO') 

    if b_any('test' in x.lower() for x in permissions):
        site_slugs.append('TB') 

    if b_any('livraria' in x.lower() for x in permissions):
        site_slugs.append('LC') 

    if b_any('audio' in x.lower() for x in permissions):
        site_slugs.append('AU') 
    return site_slugs