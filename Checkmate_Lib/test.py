#from kobo_parser import KoboSite
from checkmate import BookSite
from checkmate import get_book_site


def parseAll(self, site, content):
        
        print("Title: ")
        site.titleParser(content)
        print("Authors: ")
        site.authorsParser(content)
        print("ISBN: ")
        site.isbnParser(content)
        print("Format: ")
        site.formatParser(content)
        print("Description: ")
        site.descParser(content)
        print("Subtitle: ")
        site.subtitleParser(content)
        print("Series: ")
        site.seriesParser(content)
        print("Volume: ")
        site.volumeParser(content)
        print("Image URL: ")
        site.imageUrlParser(content)
        print("Ready Status: ")
        site.saleReadyParser(content)
        print("Image Saved")
        site.imageParser(content)



def main():
    slug = imput("Enter a site slug.")
    site = get_book_site(slug)
    url = input("Enter a url: ")
    content = fetch(url)
     
    site_book_data = site.get_book_data_from_site(url)
    site_book_data.print_all()


 #url = "https://www.kobo.com/us/en/ebook/the-lion-the-witch-and-the-wardrobe-1"

def fetch(url):
    response = requests.get(url)
    return response.content
    

if __name__ == "__main__":
    main()


