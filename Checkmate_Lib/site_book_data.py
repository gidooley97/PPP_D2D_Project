
class SiteBookData:

    def __init__():
        self.format=""
        self.book_title=""
        self.book_img="" #need to figure how to store
        self.book_img_url= ""
        self.isbn_13=""
        self.description=""
        self.series=""
        self.volume=""
        self.subtitle=""
        self.authors=""
        self.book_id= ""
        self.site_slug=""
        self.parse_status=""
        self.url=""
        self.content=""
        self.ready_for_sale=""
        self.extra=""
      
        




    def __init__(self, formt, book_title,book_img, book_img_url,
        isbn_13, description, series, volume_number,subtitle, authors,
        book_id, site_slug, parse_status, url, content, ready_for_sale, extra):
        self.format=formt
        self.book_title=book_title
        self.book_img=book_img #need to figure how to store
        self.book_img_url= book_img_url
        self.isbn_13=isbn_13
        self.description=description
        self.series=series
        self.volume=volume_number
        self.subtitle=subtitle
        self.authors=authors
        self.book_id= book_id
        self.site_slug=site_slug
        self.parse_status=parse_status
        self.url=url
        self.content=content
        self.ready_for_sale=ready_for_sale
        self.extra=extra
    



    def print_all(self):
        print("Slug: " + self.site_slug)
        print("Format: " + self.format)
        print("Title: " + self.book_title)
        print("Authors: " + ','.join(self.authors))
        print("Series: " + self.series)
        print("Volume:  " + self.volume)
        print("ISBN: " + self.isbn_13)
        print("Description: " + self.description)
        print("Book Image URL: " + self.book_img_url)
        print("Sale Status: " + self.ready_for_sale)


