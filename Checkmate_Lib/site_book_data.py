

class SiteBookData:
    """
    initialiaze all attributes to None.

    Helps us know if the info was was found or not. 
    params:
        None
    return:
        None
    """
    def __init__(self,**kwargs):
        self.format=None
        self.book_title=None
        self.book_img=None
        self.book_img_url= None
        self.isbn_13=None
        self.description=None
        self.series=None
        self.volume=None
        self.subtitle=None
        self.authors=[]
        self.book_id= None
        self.site_slug=None
        self.parse_status=None
        self.url=None
        self.content=None
        self.ready_for_sale=None
        self.extra=None

        if 'format' in kwargs:
            self.format = kwargs['format']
        if 'book_title' in kwargs:
            self.book_title = kwargs['book_title']
        if 'book_img' in kwargs:
            self.book_img = kwargs['book_img']
        if 'isbn_13' in kwargs:
            self.isbn_13 = kwargs['isbn_13']
        if 'description' in kwargs:
            self.description = kwargs['description']
        if 'series' in kwargs:
            self.series = kwargs['series']
        if 'volume' in kwargs:
            self.volume = kwargs['volume']
        if 'subtitle' in kwargs:
            self.subtitle = kwargs['subtitle']
        if 'authors' in kwargs:
            self.authors = kwargs['authors']
        if 'book_id' in kwargs:
            self.book_id = kwargs['book_id']
        if 'site_slug' in kwargs:
            self.site_slug = kwargs['site_slug']
        if 'parse_status' in kwargs:
            self.parse_status = kwargs['parse_status']
        if 'book_img_url' in kwargs:
            self.book_img_url = kwargs['book_img_url']
        if 'content' in kwargs:
            self.content = kwargs['content']   
        if 'ready_for_sale' in kwargs:
            self.ready_for_sale = kwargs['ready_for_sale']
        if 'format' in kwargs:
            self.format = kwargs['format'] 
        if 'price' in kwargs:
            self.price = kwargs['price'] 
        if 'url' in kwargs:
            self.url = kwargs['url'] 
        if 'extra' in kwargs:
            self.extra = kwargs['extra']
    """
    prints fields of the book.

    Helps in testing.
    params:
        None
    return:
        None
    """
    def print_all(self):
        print("Format: " , self.format if self.format!=None else 'Not found')
        print("Title: " ,self.book_title if self.book_title !=None else 'Not found')
        print("Subtitle: " ,self.subtitle if self.subtitle !=None else 'Not found')
        print("Authors: " , ','.join(self.authors) if self.authors else 'Not found')
        print("Series: " , self.series if self.series !=None else 'Not found')
        print("Volume:  ", self.volume if self.volume != None else 'Not found')
        print("ISBN: " , self.isbn_13 if self.isbn_13 != None  else 'Not found')
        print("Description: " , self.description if self.description !=None else 'Not found')
        print("Book Image URL: " , self.book_img_url if self.book_img_url!=None else 'Not found')
        print("Sale Status: ",  self.ready_for_sale if self.ready_for_sale!=None else 'Not found')
        print("parse status: ", self.parse_status if self.parse_status else 'Not found')
        print("Direct book Url: ", self.url if self.url else 'Not found')
        print("Extra: ", self.extra if self.extra else 'Not found')

"""
convert isbn10 to isbn13.

1. take the 10 digit ISBN (10 digits)
2. drop the last character (9 digits)
3. tack on "978" to the front (12 digits)
4. calculate a new check digit and tack it on to the end (13 digits)
params:
    isbn 10
return:
    isbn 13
"""
def isbn_10_to_isbn_13(isbn_10):
    isbn_10 = isbn_10.strip()
    if len(isbn_10)==13:
        return isbn_10
    if len(isbn_10)!=10 or not isbn_10.isdigit():
        return None
    x = isbn_10[:9]#remove 10th digits
    y = '978'+x  # add '978'in front of the remaining 9  digits
    total = 0
    count =0
    #loop through the digits.digits with odd digits are multiplied by 3 and even ones are multiplied by 1.
    #sum all the results
    for c in y: 
        num =int(c)
        if count % 2:
            total +=num*3
        else:
            total+=num*1
        count+=1

    t = total%10 #get the modulus of the sum. 
    t = abs(t-10) #finally, compute the absolute value of subtract the result from 10
    y = y+str(t)  
    return y

    




   





