import os
import sys
import book_dao
from bson import Decimal128

# menu.py - Book Manager Software
# Author: Ben Blake

# The script utilizes functions from book_dao.py for database operations and provides an interactive
# menu system for users to manage the book database efficiently.

# The system allows users to perform the following actions:
# - Add a new publisher with information such as name, phone, and city.
# - Add a new book with details including ISBN, title, year, published_by, previous edition, and price.
# - Edit the information of an existing book.
# - Delete a book from the database.
# - Search for books based on various criteria.

# Search Options:
# 1. All books. Based on title.
# 2. Based on publisher.
# 3. Based on price range (min and max).
# 4. Based on title and publisher.

menu_options = {
    1: 'Add a Publisher',
    2: 'Add a Book',
    3: 'Edit a Book',
    4: 'Delete a Book',
    5: 'Search Books',
    6: 'Exit'
}

search_menu_options = {
    1: 'All books. Based on title',
    2: 'Based on publisher',
    3: 'Based on price range (min and max)',
    4: 'Based on title and publisher'
}


def add_publisher():
    # Adds a new publisher to the database based on user input. The function prompts the user to enter the name,
    # phone number, and city of the new publisher. It then creates a dictionary representing the new publisher and calls
    # the insert_publisher function from book_dao to add the publisher to the database.
    print('')

    publisher_name = input('Enter the name of the publisher: ')
    publisher_phone = input('Enter the phone number of the publisher: ')
    publisher_city = input('Enter the city of the publisher: ')

    new_publisher = {
        'name': publisher_name,
        'phone': publisher_phone,
        'city': publisher_city
    }

    result = book_dao.insert_publisher(new_publisher)

    if result:
        print(f'Publisher {publisher_name} added successfully!')
    else:
        print('Failed to add the publisher.')

    print('')


def add_book():
    # Adds a new book to the database based on user input.
    # The function prompts the user to enter information such as ISBN, title, year, publisher,
    # previous edition, and price of the new book. It then creates a dictionary representing the
    # new book and calls the insert_book function from book_dao to add the book to the database.
    print('')

    isbn = input('Enter the ISBN of the book: ')
    title = input('Enter the title of the book: ')
    year = input('Enter the year of the book: ')
    published_by = input('Enter the publisher of the book: ')
    previous_edition = input('Enter the previous edition of the book: ')
    price = float(input('Enter the price of the book: '))

    new_book = {
        'ISBN': isbn,
        'title': title,
        'year': year,
        'published_by': published_by,
        'previous_edition': previous_edition,
        'price': Decimal128(str(price))
    }

    result = book_dao.insert_book(new_book)

    if result:
        print(f'Book {title} added successfully!')
    else:
        print('Failed to add the book.')

    print('')


def edit_book():
    # Edits an existing book in the database based on user input.
    # The function prompts the user to enter the ISBN of the book to edit. It checks if the book
    # exists, displays its information, and then allows the user to enter new information for
    # the title, year, publisher, previous edition, and price. The update_book function from
    # book_dao is then called to update the book in the database.
    print('')

    isbn = input('Enter the ISBN of the book you want to edit: ')

    # Check if the book exists
    existing_book = book_dao.find_by_isbn(isbn)
    if not existing_book:
        print(f'Book with ISBN {isbn} not found.')
        return

    # Display existing book information
    print('Existing Book Information:')
    print(existing_book)

    # Get new information
    title = input('Enter the new title (or press Enter to keep the existing title): ')
    year = input('Enter the new year (or press Enter to keep the existing year): ')
    published_by = input('Enter the new publisher (or press Enter to keep the existing publisher): ')
    previous_edition = input('Enter the new previous edition (or press Enter to keep the existing edition): ')
    price = input('Enter the new price (or press Enter to keep the existing price): ')

    # Update only non-empty fields
    updated_book = {}
    if title:
        updated_book['title'] = title
    if year:
        updated_book['year'] = year
    if published_by:
        updated_book['published_by'] = published_by
    if previous_edition:
        updated_book['previous_edition'] = previous_edition
    if price:
        updated_book['price'] = Decimal128(str(float(price)))

    result = book_dao.update_book(isbn, updated_book)

    if result:
        print(f'Book with ISBN {isbn} updated successfully!')
    else:
        print('Failed to update the book.')

    print('')


def delete_book():
    # Deletes an existing book from the database based on user input.
    # The function prompts the user to enter the ISBN of the book to delete. It checks if the book
    # exists, displays its information, and then asks for confirmation before calling the
    # delete_book function from book_dao to delete the book from the database.
    print('')

    isbn = input('Enter the ISBN of the book you want to delete: ')

    # Check if the book exists
    existing_book = book_dao.find_by_isbn(isbn)
    if not existing_book:
        print(f'Book with ISBN {isbn} not found.')
        return

    # Display existing book information
    print('Book Information:')
    print(existing_book)

    confirmation = input('Are you sure you want to delete this book? (y/n): ')
    if confirmation.lower() != 'y':
        print('Deletion canceled.')
        return

    result = book_dao.delete_book(isbn)

    if result:
        print(f'Book with ISBN {isbn} deleted successfully!')
    else:
        print('Failed to delete the book.')

    print('')


def search_books():
    # Initiates a search for books based on user input.
    # The function prints the search menu and prompts the user to select a search option.
    # It then calls the corresponding search function based on the user's choice.
    print_search_menu()
    search_option = ''

    try:
        search_option = int(input('Please select a function, type [1 - 4] and press enter: '))
    except KeyboardInterrupt:
        print('Interrupted . . .')
        sys.exit(0)
    except ValueError:
        print('Wrong input. Please enter a number . . .')

    if search_option == 1:
        search_all_books()
        search_by_title()
    elif search_option == 2:
        search_by_publisher()
    elif search_option == 3:
        search_by_price_range()
    elif search_option == 4:
        search_by_title_and_publisher()
    else:
        print('Invalid option. Please enter a number between 1 and 4.')


def print_search_menu():
    # Prints the search menu header and options.
    # The function calculates the necessary dashes to center the header text and prints the
    # formatted header. It then prints each search menu option along with its corresponding number.
    print('')

    header_text = 'Search Books'
    console_width = os.get_terminal_size().columns  # Get width of console
    dash_count = (console_width - len(header_text)) // 2  # Calculate dashes needed on sides to center text
    print('=' * dash_count + header_text + '=' * dash_count)  # Print header

    for key in search_menu_options.keys():
        print(str(key) + '.' + search_menu_options[key], end='  ')

    print('')


def search_all_books():
    # Searches for and prints all books in the database.
    # The function calls the find_all function from book_dao and prints the ISBNs and titles
    # of all books returned from the database.
    results = book_dao.find_all()

    print('The following are the ISBNs and titles of all books.')
    for item in results:
        print(item['ISBN'], item['title'])


def search_by_title():
    # Searches for books by the exact title entered by the user.
    # The function prompts the user to enter an exact book title and calls the find_by_title
    # function from book_dao to search for books with that title in the database.
    print('')

    title = input('Enter the exact book title:')
    results = list(book_dao.find_by_title(title))

    if len(results) != 0:
        print('We found the following matching titles for you.')
        for item in results:
            print(item['ISBN'], item['title'])
    else:
        print('The title you wanted does not exist in our database.')

    print('')


def search_by_publisher():
    # Searches for books published by the publisher entered by the user.
    # The function prompts the user to enter a publisher and calls the find_by_publisher
    # function from book_dao to search for books published by that publisher in the database.
    print('')

    publisher = input('Enter the publisher you want to search for:')
    results = list(book_dao.find_by_publisher(publisher))

    if len(results) != 0:
        print(f'We found the following books from publisher {publisher}:')
        for item in results:
            print(item['ISBN'], item['title'])
    else:
        print(f'No books found from publisher {publisher}.')

    print('')


def search_by_price_range():
    # Searches for books within the price range entered by the user.
    # The function prompts the user to enter minimum and maximum prices and calls the
    # find_by_price_range function from book_dao to search for books within that price
    # range in the database.
    print('')
    min_price = 0
    max_price = 0

    try:
        min_price = float(input('Enter the minimum price:'))
        max_price = float(input('Enter the maximum price:'))
    except ValueError:
        print("Invalid input. Please enter a valid number.")

    results = list(book_dao.find_by_price_range(min_price, max_price))

    if len(results) != 0:
        print(f'We found the following books in the price range ${min_price} to ${max_price}:')
        for item in results:
            print(item['ISBN'], item['title'])
    else:
        print(f'No books found in the specified price range.')

    print('')


def search_by_title_and_publisher():
    # Searches for books with a specific title and published by a specific publisher.
    # The function prompts the user to enter an exact book title and a publisher.
    # It then calls the find_by_title_and_publisher function from book_dao to search
    # for books with the specified title and publisher in the database.
    print('')

    title = input('Enter the exact book title:')
    publisher = input('Enter the publisher:')

    results = list(book_dao.find_by_title_and_publisher(title, publisher))

    if len(results) != 0:
        print(f'We found the following books with title "{title}" from publisher {publisher}:')
        for item in results:
            print(item['ISBN'], item['title'])
    else:
        print(f'No books found with title "{title}" from publisher {publisher}.')

    print('')


def print_menu():
    # Prints the main menu header and options.
    # The function calculates the necessary dashes to center the header text and prints
    # the formatted header. It then prints each main menu option along with its corresponding
    # number, providing a visual representation of the available functionalities.
    print('')

    header_text = 'Book Manager Software'
    console_width = os.get_terminal_size().columns  # Get width of console
    dash_count = (console_width - len(header_text)) // 2  # Calculate dashes needed on sides to center text
    print('-' * dash_count + header_text + '-' * dash_count)  # Print header

    for key in menu_options.keys():
        print(str(key) + '.' + menu_options[key], end='  ')

    print('')


if __name__ == '__main__':
    # Entry point for the Book Manager Software.
    # The code within this block is executed when the script is run as the main program.
    # It presents a loop that continuously displays the main menu using the print_menu function.
    # The user is prompted to select a function by entering a number. The corresponding function
    # is then executed based on the user's choice, providing an interactive interface.
    # The loop continues until the user chooses to exit (option 6).
    while True:
        print_menu()
        option = ''

        try:
            option = int(input('Please select a function, type [1 - 6] and press enter: '))
        except KeyboardInterrupt:
            print('Interrupted . . .')
            sys.exit(0)
        except ValueError:
            print('Wrong input. Please enter a number . . .')

        if option == 1:
            add_publisher()
        elif option == 2:
            add_book()
        elif option == 3:
            edit_book()
        elif option == 4:
            delete_book()
        elif option == 5:
            search_books()
        elif option == 6:
            print('Thanks your for using our database services! Bye')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 6.')
