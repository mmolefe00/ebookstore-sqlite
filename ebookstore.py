"""
This project demonstrates how sqlite can be useful to a bookstore clerk.
It allows a clerk to add new books, update book information, search and delete books from a sql database.
It is structured to output a menu as well as format the requested book data in a readable manner to the clerk.
"""

# ==== establishing database connection =====

import sqlite3                                      # import
db = sqlite3.connect('ebookstore')                  # create database file
cursor = db.cursor()                                # create cursor
db.commit()                                         # commit command to database
print('<< Database Connection Established >>')      # validation statement.


# ==== Create Table =====
cursor.execute('''CREATE TABLE IF NOT EXISTS ebookstore(
    id INTEGER,
    title TEXT,
    author TEXT,
    qty INTEGER
    );''')

db.commit()                                         # commit command to database
print('<< EBookstore Table Created. >>\n\n')        # validation statement


# ==== functions =====
def add_book():
    # empty list of books: id, title, author, qty
    # to be empty with each time the function is run - to avoid duplicate commitments.
    books = []

    while True:
        sub_menu = input('''\nWould you like to enter a new book or commit your added books to the database?
Note:   Please only commit to database once you have added new books.
        Books not committed to the database will be lost.
            
    n - add new book
    c - commit to database
    e - exit to main menu
    :\t''').lower()

        # add new book
        if sub_menu == 'n':

            # get book data from user
            print('Please enter the following book details:')
            id_ = int(input(' - Book ID:\t'))
            title_ = input(' -  Title:\t')
            author_ = input(' - Author:\t')
            qty_ = int(input(' - Quantity:\t'))


            book = id_, title_, author_, qty_   # format book data to add to books list
            books.append(book)                  # append to books list
            pass                                # note: books will be added to list until user selects commit.

        # commit added books
        elif sub_menu == 'c':

            # formatted summative output to show which books are being committed to the database.
            underline = '----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----'
            print('\nCommitting the following Books:')
            print(underline)
            for book in books:
                print(f"""ID: {book[0]}\tQuantity: {book[3]}\tTitle: '{book[1]}' by {book[2]}\t""")
                # chose ID, QTY, Title by Author for formatting purposes (variable title & author lengths)
            print(underline)

            # commit the books list to the database using execute many.
            cursor.executemany('''
            INSERT INTO ebookstore(id, title, author, qty)
            VALUES (?,?,?,?)''', books)

            # commit to database
            db.commit()

            # validate commitments to user
            print('\n<< Books Committed>>\n')
            break

        # exit to main menu
        elif menu == 'e':
            break

        else:
            print('Oops! Please enter a valid option.')

def update_book():
    # select primary key (book ID) for book.
    id_ = int(input('Please enter the book ID (e.g. 3001):\t'))

    # display current book data to user
    # format view output
    underline = '----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----'
    print('\n' + underline)
    print('SELECTED BOOK:')
    print(underline)
    print('\nID:\t\tQTY:\t"TITLE" by AUTHOR:')

    # select and output from database
    cursor.execute('SELECT * FROM ebookstore WHERE id = ?;', (id_,))
    for row in cursor:
        print('{0}\t{3}\t\t"{1}" BY {2}.'.format(row[0], row[1], row[2], row[3]))
        # chose ID, QTY, Title by Author for formatting purposes (variable title & author lengths)
    print(underline)

    # user input to change data
    while True:
        submenu = input('''\n\t- What information would you like to change?
    t - Title
    a - Author
    q - Quantity
    e - Exit
    :''')

        if submenu == 't':
            # get new title input
            new_title = input("New Title:\t")

            # update change in database
            cursor.execute('''UPDATE ebookstore 
            SET title = ? WHERE id = ?; ''', (new_title, id_))
            db.rollback()       # rollback changes since last commit
            pass

        elif submenu == 'a':
            # get new author input
            new_author = input("New Author:\t")

            # update change in database
            cursor.execute('''UPDATE ebookstore 
            SET author = ? WHERE id = ?; ''', (new_author, id_))
            db.rollback()       # rollback changes since last commit
            pass

        elif submenu == 'q':
            # get new quantity input
            new_quantity = int(input("New Quantity:\t"))

            # update change in database
            cursor.execute('''UPDATE ebookstore 
            SET qty = ? WHERE id = ?; ''', (new_quantity, id_))
            db.rollback()       # rollback changes since last commit
            pass

        elif submenu == 'e':
            break

        else:
            print("Oops! Please choose a valid option.")

    # display updated book data to user
    # format view output
    underline = '----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----'

    # display updated book data to user
    print('\n' + underline)
    print('UPDATED BOOK:')
    print(underline)
    print('ID:\t\tQTY:\t"TITLE" by AUTHOR:')

    # select and output from database
    cursor.execute('SELECT * FROM ebookstore WHERE id = ?;', (id_,))
    for row in cursor:
        print('{0}\t{3}\t\t"{1}" BY {2}.'.format(row[0], row[1], row[2], row[3]))
        # chose ID, QTY, Title by Author for formatting purposes (variable title & author lengths)
    print(underline)


def delete_books():
    # select primary key (book ID) for book.
    id_ = int(input('\nPlease enter the book ID (e.g. 3001):\t'))

    # display current book data to user
    # format view output
    underline = '----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----'
    print('\n' + underline)
    print('SELECTED BOOK:')
    print(underline)
    print('ID:\t\tQTY:\t"TITLE" by AUTHOR:')

    # select and output from database
    cursor.execute('SELECT * FROM ebookstore WHERE id = ?;', (id_,))
    for row in cursor:
        print('{0}\t{3}\t\t"{1}" BY {2}.'.format(row[0], row[1], row[2], row[3]))
        # chose ID, QTY, Title by Author for formatting purposes (variable title & author lengths)
    print(underline + "\n")

    # get user confirmation
    while True:
        confirmation = input(f'''Are you sure you want to delete this book?
y - yes
n - no
:\t''')
        # if yes, delete from database
        if confirmation == 'y':
            cursor.execute('DELETE FROM ebookstore WHERE id = ?;', (id_,))
            db.commit()     # commit
            break

        # if no, exit to main menu
        elif confirmation == 'n':
            break

        # if incorrect input, display error message
        else:
            print('\nPlease enter a valid option.')


def search_book():
    # select primary key (book ID) for book.
    id_ = int(input('\nPlease enter the book ID (e.g. 3001):\t'))

    # display current book data to user
    # format view output
    underline = '----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----'
    print('\n' + underline)
    print('CURRENT BOOK:')
    print(underline)
    print('ID:\t\tQTY:\t"TITLE" by AUTHOR:')

    # select and output from database
    cursor.execute('SELECT * FROM ebookstore WHERE id = ?;', (id_,))
    for row in cursor:
        print('{0}\t{3}\t\t"{1}" BY {2}.'.format(row[0], row[1], row[2], row[3]))
        # chose ID, QTY, Title by Author for formatting purposes (variable title & author lengths)
    print(underline + "\n")


def view_all():
    # format view output
    underline = '----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----'
    print("\n\nLIBRARY:")
    print(underline)
    print('ID:\t\tQTY:\t"TITLE" by AUTHOR:')
    print(underline)

    # select data and format output with loop from database
    cursor.execute('SELECT id, title, author, qty FROM ebookstore;')
    for row in cursor:
        print('{0}\t{3}\t\t"{1}" BY {2}.'.format(row[0], row[1], row[2], row[3]))
        # chose ID, QTY, Title by Author for formatting purposes (variable title & author lengths)

    # format end of table
    print(f'{underline}\n')


# ==== main menu =====

greeting = ('''Hello! Welcome to our eBookstore database
Where you can add, update, delete and search books.''')
print(greeting)

while True:
    menu = input('''\n\n=== MAIN MENU ===
    Please select an option: (1-6)
    1 - add new books to database
    2 - update book information
    3 - delete books from database
    4 - search book in database
    5 - view all books
    6 - exit
    : ''')

    # add books
    if menu == "1":
        add_book()
        pass

    # update books
    elif menu == "2":
        update_book()
        pass


    # delete books
    elif menu == "3":
        delete_books()
        pass

    # search books
    elif menu == "4":
        search_book()
        pass

    # view all books
    elif menu == "5":
        view_all()

    # exit
    elif menu == "6":
        print("\nGoodbye!")                     # farewell
        db.close()                              # close database
        print('\n\n<< Database closed. >>')     # validation statement
        break

    # error message
    else:
        print('\nOops! Please enter a valid option.')
