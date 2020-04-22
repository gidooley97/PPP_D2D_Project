import unittest
import os
import sys
from pathlib import Path
# getting around the problem of importing modules.
root= str(Path(__file__).resolve().parents[2])
dir_of_interest = root+'/Checkmate_Lib'
modules = {}
sys.path.append(dir_of_interest)
for module in os.listdir(dir_of_interest):
    if '.py' in module and '.pyc' not in module:
        current = module.replace('.py', '')
        modules[current] = __import__(current)

get_book_site = modules['checkmate'].get_book_site
SiteBookData = modules['site_book_data'].SiteBookData
#####################################################


"""
Unittest on Audiobooks parser. The following Test case 

class runs tests on the get_book_data from_site and
find_matches_from_site functions.
"""
class TestAudioBooksParser(unittest.TestCase):
    def test_get_book_data_from_site(self):
        file = open("lord_jim_audio.html", "r",encoding='UTF-8')
        content = file.read().encode('UTF-8')
        file.close()
        book_site = get_book_site("AU")
        site_book_data = book_site.get_book_data_from_site(url=None, content=content)
        site_book_data.description =None
        site_book_data.book_img =None

        site_book_data_expected = SiteBookData(book_title="Lord Jim", format="Audiobook", authors=["Joseph Conrad"],
                        description =None, book_img_url="http://covers.audiobooks.com/images/covers/full/9789176391921.jpg",
                        parse_status="PARTIALLY PARSED", site_slug = "AU", url=None, extra={"Narrator":["Stewart Wills"]})
        
        self.assertEqual( site_book_data, site_book_data_expected)
       
        

    def test_find_book_matches_at_site(self):
        book_site = get_book_site("AU")
        site_book_data = SiteBookData (book_title="Lord Jim")
        urls = book_site.find_book_matches_at_site(site_book_data, pages =1, is_unittest =True)
        urls_expected =['https://www.audiobooks.com/audiobook/lord-jim/427769', 'https://www.audiobooks.com/audiobook/lord-jim/117787', 
        'https://www.audiobooks.com/audiobook/lord-jim/165035', 'https://www.audiobooks.com/audiobook/lord-jim/272485',
        'https://www.audiobooks.com/audiobook/lord-jim/248483', 'https://www.audiobooks.com/audiobook/lord-jim/199173', 
        'https://www.audiobooks.com/audiobook/lord-jim/289636', 'https://www.audiobooks.com/audiobook/lord-jim/60739', 
        'https://www.audiobooks.com/audiobook/lord-jim/320514', 'https://www.audiobooks.com/audiobook/lord-jim/230218', 
        'https://www.audiobooks.com/audiobook/lord-jim/58185', 'https://www.audiobooks.com/audiobook/lord-jim/165403', 
        'https://www.audiobooks.com/audiobook/n-b-c-university-theater-lord-jim/410161', 
        'https://www.audiobooks.com/audiobook/killers-alibi/347891', 
        'https://www.audiobooks.com/audiobook/dawn-watch-joseph-conrad-in-a-global-world/307724',
        'https://www.audiobooks.com/audiobook/youth-a-narrative/199177', 
        'https://www.audiobooks.com/audiobook/joseph-conrad-the-short-stories/297190', 
        'https://www.audiobooks.com/audiobook/youth/429230', 'https://www.audiobooks.com/audiobook/youth-a-narrative/427638',
        'https://www.audiobooks.com/audiobook/youth-a-narrative/365525']
        self.assertCountEqual(urls,urls_expected)


if __name__=='__main___':
    unittest.main()


"""
Run "python3 -m unittest test_audiobooks.py" in the terminal to run all unit tests.
"""