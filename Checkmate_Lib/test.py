from checkmate import get_book_site #this is the only import we need to use the library

#write tests 

def main():
    slug = 'LC'
    book_site = get_book_site(slug)
   
    #url1 = "https://www.kobo.com/us/en/ebook/lord-8"
    url2 = "https://www3.livrariacultura.com.br/a-fenda-2012668782/p"
    print("\n\nUrl 1:")
    book_site_data = book_site.get_book_data_from_site(url2)
    book_site_data.print_all()
    matches = book_site.find_book_matches_at_site(book_site_data)
    for book in matches:
        print("score", str(book[0]))
        book[1].print_all()


   

if __name__ == "__main__":
    main()


