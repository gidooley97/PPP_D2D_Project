from site_book_data import SiteBookData
import io
from lxml import etree
import requests
#from PIL import Image
import urllib.request

class GoogleBooks:
    def __init__(self):
        self.site_slug = "GB"
        self.search_url = "https://www.books.google.com/"
        self.url_to_book_detail = "https://www.books.google.com/book?vid=ISBN"
        self.match_list = []

    def get_book_Data_from_site(self, url):
        content = requests.get(url).content
        parser = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(content), parser)
        root = tree.getroot()
        title = self.titleParser(root)
        img_url = self.imageUrlParser(root)
        #img = self.imageParser(root)
        isbn13 = self.isbnParser(root)
        desc = self.descriptionParser(root)
        series = self.seriesParser(root)
        subtitle = self.subtitleParser(root)
        authors = self.authorsParser(root)
        site_slug = self.site_slug
        content = content
        url = url
        parse_status = self.get_parse_status(title, isbn13, desc, authors)
        ready_for_sale = self.sales_flag_parser(root)
        extra = self.extraParser(root)
        book_site_data = SiteBookData("format", title, "img", img_url, isbn13, desc, series, "None", subtitle, authors, "None", site_slug, parse_status, url, content, ready_for_sale, extra)
        return book_site_data

    def convert_book_id_to_url(self, book_id):
        return self.url_to_book_detail+book_id

    def match_percentage(self, site_book1, site_book2):
        return super().match_percentage(site_book1, site_book2)

    def titleParser(self, root):
        title = root.xpath("//h1[@class='booktitle']//span//span")[0].text
        print(title)
        return title


    def subtitleParser(self, root):
        subtitle = ''
        if root.xpath("//h1[@class='booktitle']//span[2]//span"):
            subtitle = root.xpath("//h1[@class='booktitle']//span[2]//span")[0].text
        print(subtitle)
        return subtitle

    def seriesParser(self, root):
        series = ''
        if root.xpath("//td[@class='metadata_value']/a[1]/i/span"):
            series = root.xpath("//td[@class='metadata_value']/a[1]/i/span")[0].text
        print(series)
        return series

    def authorsParser(self, root):
        author_elements = root.xpath("//div[@class='bookinfo_sectionwrap']/div[1]/a/span")
        authors = []
        for auth_element in author_elements:
            authors.append(auth_element.text)
            print(auth_element.text)
        return authors

    def isbnParser(self, root):
        try:
            if root.xpath("//tr[4]//td[@class='metadata_label']//span")[0].text == 'ISBN':
                isbn_element = root.xpath("//tr[4]//td[@class='metadata_value']//span")[0].text
            elif root.xpath("//tr[5]//td[@class='metadata_label']//span")[0].text == 'ISBN':
                isbn_element = root.xpath("//tr[5]//td[@class='metadata_value']//span")[0].text
            elif root.xpath("//tr[6]//td[@class='metadata_label']//span")[0].text == 'ISBN':
                isbn_element = root.xpath("//tr[6]//td[@class='metadata_value']//span")[0].text
            elif root.xpath("//tr[7]//td[@class='metadata_label']//span")[0].text == 'ISBN':
                isbn_element = root.xpath("//tr[7]//td[@class='metadata_value']//span")[0].text
            isbns = str.split(isbn_element)
            print(isbns[1])
            return isbn_element
        except:
            print("None found")
            return "None found"

    def descriptionParser(self, root):
        description = ''
        if root.xpath("//*[@id='synopsistext']"):
            description = root.xpath("//*[@id='synopsistext']")[0].text
        print(description)
        return description

    def imageUrlParser(self, root):
        imgUrl_element = root.xpath("//*[@id='summary-frontcover']/@src")[0]
        print(imgUrl_element)
        return imgUrl_element

    #def imageParser(self, root):
     #   url = self.imageUrlParser(root)
      #  response = requests.get(url)
       # image = Image.open(urllib.request.urlopen(url))
        #image.save("search.jpg")

    def sales_flag_parser(self, root):
        sale_flag = 0
        status = ""
        sales_element = root.xpath("//*[@id='gb-get-book-content']")[0].text
        if "print" in sales_element.lower():
            sale_flag = 0
            status = "Find Print"
        elif "ebook" in sales_element.lower():
            status = 0
            status = "Buy Now"
        elif "pre-order" in sales_element.lower():
            sale_flag = 1
            status = "Pre-order"
        print(status)
        return status

    def extraParser(self, root):
        return {}

    def get_parse_status(self, title, isbn13, desc, authors):
        if title and isbn13 and desc and authors:
            return "UNSUCCESSFUL"
        return "FULLY PARSED"


    def parseAll(self, site, root):
        print("Title: ")
        site.titleParser(root)
        print("Subtitle: ")
        site.subtitleParser(root)
        print("Series: ")
        site.seriesParser(root)
        print("Authors: ")
        site.authorsParser(root)
        print("ISBN: ")
        site.isbnParser(root)
        print("Description: ")
        site.descriptionParser(root)
        print("Image Url: ")
        site.imageUrlParser(root)
        print("Image Saved")
        #site.imageParser(root)
        print("Sales Flag: ")
        site.sales_flag_parser(root)

def main():
    #With subtitle
    #url = 'https://books.google.com/books?vid=ISBN9781423196372'
    #Without subtitle
    #url = "https://books.google.com/books?vid=ISBN9780007269709"
    #Preorder
    #url = "https://books.google.com/books?vid=ISBN9781338635188"
    #Volume
    url = 'https://books.google.com/books?vid=ISBN9780521070607'
    site = GoogleBooks()
    response = requests.get(url)
    content = response.content
    parser = etree.HTMLParser(remove_pis=True)
    tree = etree.parse(io.BytesIO(content), parser)
    root = tree.getroot()
    site.parseAll(site, root)

if __name__ == "__main__":
    main()