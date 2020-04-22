from checkmate import get_book_site #this is the only import we need to use the library
import requests
from site_book_data import SiteBookData

# Load a sitebook data object from a url. Then searches for 
# site matches using the book.
def run_demo():
    search_with_attr=True #Change this to true to search by attribute


    slug = 'GB'
    if search_with_attr:
        attribute="The Lord"
        bookSite = get_book_site(slug)
        book_site_data = SiteBookData(book_title = attribute)
        matches = bookSite.find_book_matches_at_site(book_site_data) # Get book matches
        for book in matches:
            print("=======================================================================================")
            print("Score: ", str(book[0]))
            book[1].print_all()

    else:
        book_site = get_book_site(slug) # seed Book Site object with slug
        url = "https://www.google.com/books/edition/The_Lord/eyK309uZ9o8C?hl=en"
        book_site_data = book_site.get_book_data_from_site(url) # Parse data from site
        book_site_data.print_all()
        matches = book_site.find_book_matches_at_site(book_site_data) # Get book matches
        for book in matches:
            print("=======================================================================================")
            print("Score: ", str(book[0]))
            book[1].print_all()
        

def main():
    run_demo()

if __name__ == "__main__":
    main()