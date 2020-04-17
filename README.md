# PPP_D2D_Project
This is the repository for Profession Python Pros D2D Project.
This repo has two folders of interest inside of the ppp_proj folder.

Use the master branch to see the full project thus far.

The PPP_Test_Bookstore folder contains the Django site for the Test Book Store.
The manage.py file is in the nested test_bookstore file.

The Checkmate_Lib folder contains the Checkmate Library. This folder contains
two other folders for organizational reasons.

The B2B_Site folder contains the business to business site that works as an interface for our Checkmate Library. Through this site you are able to make searches on an api to find books availble on sites, these sites are decided via the various parsers. Additionally the site allows for tracking of api calls made per user. 

The testing folder contains demo files for each parser.  These files can be 
ran to gather book matches from the corresponding site. (The book to get matches 
for is predefined).  The testing folder also contains a test.py file.  This is the 
primary test and allows the user to perform various functions using the library. 
There is also unit testing for audiobook parser.

The parsers folder contains files for each parser.

The BookSite.py file and the site_book_data.py file file contain the corresponding classes.

Install the requirements.txt file to install all dependencies.

  

