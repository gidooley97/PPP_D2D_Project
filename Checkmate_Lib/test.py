#from kobo_parser import KoboSite
from checkmate import BookSite
from checkmate import get_book_site
import requests
from checkmate import match_percentage
import urllib.request


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
    #slug = input("Enter a site slug.")
    slug = 'KO'
    url1 = "https://www.kobo.com/us/en/ebook/the-last-thing-she-told-me-1"
    #url2 = "https://www.kobo.com/us/en/ebook/the-select-2"
    site = get_book_site(slug)
    #url1 = input("Enter a url: ")
    #url2 = input("Enter a second url: ")

    content1 = fetch(url1)
    #content2 = fetch(url2)
     
    site_book_data1 = site.get_book_data_from_site(url1)
    #site_book_data2 = site.get_book_data_from_site(url2)
    #print("Matching Percentage: ")
    #print(match_percentage(site_book_data1,site_book_data2))
    site_book_data1.print_all()

 #url = "https://www.kobo.com/us/en/ebook/the-lion-the-witch-and-the-wardrobe-1"

def fetch(url):
    response = requests.get(url)
    return response.content
    

if __name__ == "__main__":
    main()


