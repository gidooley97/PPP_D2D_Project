# from checkmate import get_book_site #this is the only import we need to use the library
# from site_book_data import SiteBookData
import urllib

# Load a sitebook data object from a url. Then searches for 
# site matches using the book.
import os
import sys
from pathlib import Path
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



def run_demo():
    search_with_attr=False #Change this to true to search by attribute


    slug = 'AU'
    if search_with_attr:
        attribute="The Innkeeper Chronicles, Volume One"
        bookSite = get_book_site(slug)
        book_site_data = SiteBookData(book_title=attribute)
        matches= bookSite.find_book_matches_at_site(book_site_data)
        for book in matches:
            print("=======================================================================================")
            print("Score: ", str(book[0]))
            book[1].print_all()

    else:
        book_site = get_book_site(slug) # seed Book Site object with slug
        url = "https://www.audiobooks.com/audiobook/lord-halifaxs-ghost-book/206304"
        book_site_data = book_site.get_book_data_from_site(url) # Parse data from site
        book_site_data.print_all()
        matches = book_site.find_book_matches_at_site(book_site_data) # Get book matches
        for book in matches:
            print("=======================================================================================")
            print("Score: ", str(book[0]))
            book[1].print_all()

def main():
    file = open("lord_jim_audio.html", "r")
    
    print(file.read())
    run_demo()

if __name__ == "__main__":
    main()