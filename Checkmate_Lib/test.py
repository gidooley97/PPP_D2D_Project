from checkmate import get_book_site #this is the only import we need to use the library
from site_book_data import SiteBookData
from demo import run_demo

#write tests 

def main():
    driver()
  
######################## Print Functions##############################


    

# Prints out Menu for Users
def printMenu():
    print("C  -  Create New SBD to Search with")
    print("E  -  Edit SBD")
    print("V  -  View SBD")
    print("S  -  Search")
    print("L  -  Load and Run") 
    print("X  -  Exit")

# Print menu of Site Book Data Attributes to 
# edit or create
def printAttrMenu():
    print("T  -   Title")
    print("I  -   ISBN -13")
    print("S  -   Series")
    print("A  -   Author") # You can add multiple, just one at a time
    print("ST -   Subtitle")
    print("B  -   Back")

############################# End of Print Methods ###################


# searchHandler verifies the the SBD object is not empty, 
# and has at least one attribute that is not emppty that 
# can be used to search.  If the object is not valid to 
# search with, 'F' (Fail) is returned.  Else, the search 
# is preformed, the results are displayed, and no value is returned.
def searchHandler(searchSbd):
    if searchSbd == '':
        print("No valid attributes to search with")
        return 'F'

    valid_attr_count = 0;# Used to ensure the sbd has at least
    # one attribute that can be used to search

    if searchSbd.book_title != '':
        valid_attr_count += 1
    if searchSbd.isbn_13 != '':
        valid_attr_count += 1
    if searchSbd.series != '':
        valid_attr_count += 1
    if searchSbd.authors != '':
        valid_attr_count += 1
    if searchSbd.subtitle != '':
        valid_attr_count += 1
    
    if (valid_attr_count > 0): # Launch Search after ensuring there is a slug
        # Make sure there is a valid site slug
        slug = searchSbd.site_slug.upper()
        # Every object "should" have a slug, but this is just in case
        if (slug != 'KO' and slug != 'GO' and slug != 'TB' and slug != 'LC' and slug != 'SC'):
            while(slug != 'KO' and slug != 'GO' and slug != 'TB' and slug != 'LC' and slug != 'SC'):
                # if no valid slug, prompt user for new slug.
                slug = input ("No valid slug to search with. Add one now.")
                searchSbd.slug = slug # Set new slug

        # SBD should be valid now. Launch search
        book_site = get_book_site(searchSbd.site_slug)
        matches = book_site.find_book_matches_at_site(searchSbd)
        for book in matches:
            print("score", str(book[0]))
            book[1].print_all()

    else: # Fail. No valid attributes to search with
        print("No valid attributes to search with")
        return 'F'

# This function is used to create or edit a SBD.
# This function will work for either option, it just 
# replaces attribute values with the values the user enters
# A menu prompts the user to select a letter to determine which 
# attribute they want to edit/add. The value they enter is then assigned 
# to that attribute. 
def sbdEditHandler(searchSbd):
    printAttrMenu()
    option = ''
    while option != 'B':
        option = input("Select an attribute to edit.").upper()
        if (option =='T'):
            title = input("Input Title.  ")
            searchSbd.book_title = title
        elif (option == 'I'):
            isbn = input("Input ISBN.   ")
            searchSbd.isbn_13 = isbn
        elif (option == 'S'):
            series = input("Input Series.   ")
            searchSbd.series = series
        elif(option == 'A'):
            author_choice  = input( "Would you like to add on author ('A'), or replace the existing authors ('R')?  ").upper()
            # Add author to current author list
            if author_choice == 'A':
                name = input("Input authors name.   ")
                if(len(searchSbd.authors) == 0 ):
                    searchSbd.authors = [name]
                else:
                    searchSbd.authors = searchSbd.authors.append(name)
            # Replace author
            if author_choice == 'R':
                name = input("Input authors name.   ")
                searchSbd.authors = [] # Empty list
                searchSbd.authors = searchSbd.authors.append(name)

        elif(option =='ST'):
            subtitle = input("Input Subtitle.   ")
            searchSbd.subtitle = subtitle
        elif(option == 'B'):
            return searchSbd
        else:
            print("Invalid Option. Try Again.")

    return searchSbd


        

# Runs the program
def driver():
    print ("Welcome to Professonal Python Pro's Checkmate Library!")
    option = "" # Holds value that user inputs as option
    searchSbd = SiteBookData() # Site Book Data Object used to search with

    while option != 'X': # Exit on 'E'
        printMenu()
        option =  input( "Please select an option:  ").upper()
        
        if option == 'C': # Create new SBD
            # Get slug from user
            slug = ''
            while (slug != 'KO' and slug != 'GO' and slug != 'TB' and slug != 'LC' and slug != 'SC'):
                slug = input("Enter site slug.").upper()
                if(slug != 'KO' and slug != 'GO' and slug != 'TB' and slug != 'LC' and slug != 'SC'):
                    print("Invalid slug. Try Again.")

            searchSbd = SiteBookData()
            searchSbd.site_slug = slug
                
            searchSbd = sbdEditHandler(searchSbd) # Replace existing SBD
        elif option == 'E': # Edit existing SBD
            searchSbd = sbdEditHandler(searchSbd)
        elif option == 'V': # View contents of current SBD
            searchSbd.print_all()
        elif option == 'L': # Loads complete SBD form a site
            run_demo()
        elif option == 'S':
            value =  searchHandler(searchSbd)
            if  value == 'F':
                print("Invalid Site Book Data Object to search with.")
        elif option == 'X':
            exit()
        else:
            print("Invalid Option. Try Again: ")

if __name__ == "__main__":
    main()








  # slug = 'LC'
    # book_site = get_book_site(slug)
   
    # #url1 = "https://www.kobo.com/us/en/ebook/lord-8"
    # url2 = "https://www3.livrariacultura.com.br/a-fenda-2012668782/p"
    # print("\n\nUrl 1:")
    # book_site_data = book_site.get_book_data_from_site(url2)
    # book_site_data.print_all()
    # matches = book_site.find_book_matches_at_site(book_site_data)
    # for book in matches:
    #     print("score", str(book[0]))
    #     book[1].print_all()

