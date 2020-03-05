
class SiteBookData:

    def __init__():
        self.format=""
        self.book_title=""
        self.book_img="" 
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
      

    def __init__(self, formt, book_title, book_img, book_img_url,
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
    
    def __init__(self,**kwargs):
        if 'format' in kwargs.items():
            self.format = kwargs['format']
        if 'book_title' in kwargs.items():
            self.book_title = kwargs['book_title']
        if 'book_img' in kwargs.items():
            self.book_img = kwargs['book_img']
        if 'isbn_13' in kwargs.items():
            self.isbn_13 = kwargs['isbn_13']
        if 'description' in kwargs.items():
            self.description = kwargs['description']
        if 'series' in kwargs.items():
            self.series = kwargs['series']
        if 'volume' in kwargs.items():
            self.volume = kwargs['volume']
        if 'subtitle' in kwargs.items():
            self.subtitle = kwargs['subtitle']
        if 'authors' in kwargs.items():
            self.authors = kwargs['authors']
        if 'book_id' in kwargs.items():
            self.book_id = kwargs['book_id']
        if 'site_slug' in kwargs.items():
            self.site_slug = kwargs['site_slug']
        if 'parse_status' in kwargs.items():
            self.parse_status = kwargs['parse_status']
        if 'url' in kwargs.items():
            self.url = kwargs['url']
        if 'content' in kwargs.items():
            self.content = kwargs['content']   
        if 'ready_for_sale' in kwargs.items():
            self.ready_for_sale = kwargs['ready_for_sale']
        if 'format' in kwargs.items():
            self.format = kwargs['format'] 
        if 'price' in kwargs.items():
            self.price = kwargs['price'] 
        if 'url' in kwargs.items():
            self.url = kwargs['url'] 

    def print_all(self):
        print("Format: " + self.format)
        print("Title: " + self.book_title)
        print("Authors: " + ','.join(self.authors))
        print("Series: " + self.series)
        print("Volume:  " + self.volume)
        print("ISBN: " + self.isbn_13)
        print("Description: " + self.description)
        print("Book Image URL: " + self.book_img_url)
        print("Sale Status: " + self.ready_for_sale)


