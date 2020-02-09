import process_onix

def main():
    book = process_onix.test()
    print(book.isbn_13)
main()