from checkmate import get_book_site #this is the only import we need to use the library


# Load a sitebook data object from a url. Then searches for 
# site matches using the book.
def run_demo():
    search_with_attr=False #Change this to true to search by attribute


    slug = 'KO'
    if search_with_attr:
        attribute=""
        bookSite = get_book_site(slug)
        matches= bookSite.find_book_matches_by_attr_at_site(attribute)
        for book in matches:
            print("=======================================================================================")
            book.print_all()

    else:
        book_site = get_book_site(slug) # seed Book Site object with slug
        url = "https://www.kobo.com/us/en/audiobook/the-lion-the-witch-and-the-wardrobe-16"
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