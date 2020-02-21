
class SiteBookData:
    def __init__(self, format, book_title,book_img, book_img_url,
        isbn_13, description, series, volume_number,subtitle, authors,
        book_id, site_slug, parse_status, url, content, ready_for_sale, extra):
        self.format=format
        self.book_title=book_img
        self.book_img=book_img #need to figure how to store
        self.book_img_url= book_img_url
        self.isbn_13=isbn_13
        self.description=description
        self.series=series
        self.volume_number=volume_number
        self.subtitle=subtitle
        self.authors=authors
        self.book_id= book_id
        self.site_slug=site_slug
        self.parse_status=parse_status
        self.url=url
        self.content=content
        self.ready_for_sale=ready_for_sale
        self.extra=extra