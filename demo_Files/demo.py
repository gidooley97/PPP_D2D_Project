from checkmate import get_book_site #this is the only import we need to use the library
from site_book_data import SiteBookData

#demo files are used in test.py

__all__ = ['KO_demo', 'TB_demo', 'LC_demo', 'SC_demo', 'GB_demo', 'AU_demo']

# Load a sitebook data object from a url. Then searches for 
# site matches using the book.
def KO_demo():
    slug = 'KO' # Declare slug for site to search
    book_site = get_book_site(slug) # seed Book Site object with slug
    url = "https://www.kobo.com/ca/en/ebook/the-lion-the-witch-and-the-wardrobe-1"
    book_site_data = book_site.get_book_data_from_site(url) # Parse data from site
    book_site_data.site_slug = slug
    matches = book_site.find_book_matches_at_site(book_site_data) # Get book matches
    for book in matches:
        print("score", str(book[0]))
        book[1].print_all()

def TB_demo():
    slug = 'TB' # Declare slug for site to search
    book_site = get_book_site(slug) # seed Book Site object with slug
    url = "http://127.0.0.1:8000/5000/"
    book_site_data = book_site.get_book_data_from_site(url) # Parse data from site
    book_site_data.site_slug = slug
    matches = book_site.find_book_matches_at_site(book_site_data) # Get book matches
    for book in matches:
        print("score", str(book[0]))
        book[1].print_all()

def SC_demo():
    slug = 'SC' # Declare slug for site to search
    book_site = get_book_site(slug) # seed Book Site object with slug
    url = "https://www.scribd.com/book/205512285/A-Series-of-Unfortunate-Events-1-The-Bad-Beginning"
    book_site_data = book_site.get_book_data_from_site(url) # Parse data from site
    book_site_data.site_slug = slug
    matches = book_site.find_book_matches_at_site(book_site_data) # Get book matches
    for book in matches:
        print("=======================================================================================")
        print("Score: ", str(book[0]))
        book[1].print_all()

def LC_demo():
    slug = 'LC' # Declare slug for site to search
    book_site = get_book_site(slug) # seed Book Site object with slug
    url = "https://www3.livrariacultura.com.br/it-46337781/p"
    book_site_data = book_site.get_book_data_from_site(url) # Parse data from site
    book_site_data.site_slug = slug
    matches = book_site.find_book_matches_at_site(book_site_data) # Get book matches
    for book in matches:
        print("=======================================================================================")
        print("Score: ", str(book[0]))
        book[1].print_all()

def GB_demo():
    slug = 'GB' # Declare slug for site to search
    book_site = get_book_site(slug) # seed Book Site object with slug
    url = "https://books.google.com/books?id=_FjrugAACAAJ&dq=the+lord+of+the+rings&hl=en&newbks=1&newbks_redir=0&sa=X&ved=2ahUKEwiNrsjcyuPoAhVNd6wKHeHkCsgQ6AEwAHoECAAQAg"
    book_site_data = book_site.get_book_data_from_site(url) # Parse data from site
    book_site_data.site_slug = slug
    matches = book_site.find_book_matches_at_site(book_site_data) # Get book matches
    for book in matches:
        print("=======================================================================================")
        print("Score: ", str(book[0]))
        book[1].print_all()

def AU_demo():
    slug = 'AU' # Declare slug for site to search
    book_site = get_book_site(slug) # seed Book Site object with slug
    url = "https://www.audiobooks.com/audiobook/blindside/405228"
    book_site_data = book_site.get_book_data_from_site(url) # Parse data from site
    book_site_data.site_slug = slug
    matches = book_site.find_book_matches_at_site(book_site_data) # Get book matches
    for book in matches:
        print("=======================================================================================")
        print("Score: ", str(book[0]))
        book[1].print_all()