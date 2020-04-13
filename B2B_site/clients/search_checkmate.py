

import os
import sys
from pathlib import Path
from  builtins import any as b_any
from concurrent.futures import ThreadPoolExecutor
import json

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
def  process(permissions, query=0, data=0):
    if data:#json
        params = data
    else:#attribut fields
        params = query
    return search(permissions,params)    


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
    matches = []
    book_title=query.get('title')
    if query.get('authors'):
        authors = str(query.get('authors')).split(',')
    else:
        authors =None
    isbn_13 = query.get('isbn')
    book_url = query.get('book_url')
        

    if book_title is None and authors is None and  isbn_13 is None and book_url is None:
        return [] 

    all_site_slugs = get_sites(permissions)

    #having issues with searching with a book url
    if book_url and get_slug_for_url(book_url) in all_site_slugs:
        book_site = get_book_site(get_slug_for_url(book_url))
        site_book_data =book_site.get_book_data_from_site(book_url)
        book_title = site_book_data.book_title
        authors =site_book_data.authors
        isbn_13=site_book_data.isbn_13

    for site_slug in all_site_slugs:
        matches.extend(get_matches(site_slug,book_title,authors,isbn_13,book_url))
    #remember to handle json 
    # if b_any('scribd' in x for x in permissions):
    #     matches.extend(get_matches('SC',book_title,authors,isbn_13,book_url))        

    # if b_any('google' in x.lower() for x in permissions):
    #     matches.extend(get_matches('GB',book_title,authors,isbn_13,book_url))

    # if b_any('kobo' in x.lower() for x in permissions):
    #     matches.extend(get_matches('KO',book_title,authors,isbn_13,book_url))        

    # if b_any('test' in x.lower() for x in permissions):
    #     matches.extend(get_matches('TB',book_title,authors,isbn_13,book_url)) 

    # if b_any('livraria' in x.lower() for x in permissions):
    #     matches.extend(get_matches('LC',book_title,authors,isbn_13,book_url))        

    # if b_any('audio' in x.lower() for x in permissions):
    #     matches.extend(get_matches('AU',book_title,authors,isbn_13,book_url))
    
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
    # if book_url and site_slug ==is_url_for_site(book_url):
    #     print('site', site_slug)
    #     print('book_url', book_url)
    #     site_book_data =book_site.get_book_data_from_site(book_url)
    #     #site_book_data.print_all()
   
    site_book_data = SiteBookData(book_title=book_title, authors=authors,
                            isbn_13=isbn_13)

    matches =  book_site.find_book_matches_at_site(site_book_data)
    # for book in matches:
    #         print("=======================================================================================")
    #         print("Score    : ", str(book[0]))
    #         book[1].print_all()
    return list(map(lambda x:x[1],matches))


"""
Determines if the book url is for a given site.

Params:
    -book_url: book url
Returns:
    -site_slug: returns site slug if found found. else returns empty st.
"""

def get_slug_for_url(book_url):
    if 'scribd' in book_url:
        return 'SC'
    elif 'google' in book_url:
        return 'GB'
    elif 'kobo' in book_url:
        return 'KO'
    elif 'livraria' in book_url:
        return 'LC'
    elif 'audio' in book_url:
        return 'AU'
    elif 'http://127.0.0.1' in book_url:
        return 'TB'
    return ''
"""
Gets site_slugs that the user has permission to access.

Params:
    -permissions: permissions
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