from checkmate import get_book_site #this is the only import we need to use the library
from site_book_data import SiteBookData

# Load a sitebook data object from a url. Then searches for 
# site matches using the book.
def run_demo():
    search_with_attr=False #Change this to true to search by attribute
    slug = 'SC' # Declare slug for site to search
    book_site = get_book_site(slug) # seed Book Site object with slug
    if search_with_attr:
        attribute="lord"
        book_site_data = SiteBookData(book_title=attribute)
        matches = book_site.find_book_matches_at_site(book_site_data) # Get book matches
        matches.sort(key = lambda x: x[0],reverse=False)
        for book in matches:
            print("=======================================================================================")
            print("Score: ", str(book[0]))
            book[1].print_all()

    else:
        url = "https://www.scribd.com/book/377941942/John"
        book_site_data = book_site.get_book_data_from_site(url) # Parse data from site
        book_site_data.site_slug = slug
        matches = book_site.find_book_matches_at_site(book_site_data) # Get book matches
        for book in matches:
            print("=======================================================================================")
            print("Score: ", str(book[0]))
            book[1].print_all()

def main():
    run_demo()

if __name__ == "__main__":
    main()