from pymongo_connector import book_collection, publisher_collection
from bson import Decimal128


# book_dao.py
# Author: Ben Blake

# This script provides functions to interact with the MongoDB collection for book and publisher management.

def find_all():
    # Retrieves all books from the book collection.

    results = book_collection.find()
    return results


def find_by_title(book_title):
    # Retrieves books from the book collection based on the given title.

    results = book_collection.find({'title': book_title})
    return results


def find_by_publisher(publisher):
    # Retrieves books from the book collection published by the specified publisher.

    results = book_collection.find({'published_by': publisher})
    return results


def find_by_price_range(min_price, max_price):
    # Retrieves books from the book collection within the specified price range.

    results = book_collection.find({'price': {'$gte': Decimal128(str(min_price)), '$lte': Decimal128(str(max_price))}})
    return results


def find_by_title_and_publisher(title, publisher):
    # Retrieves books from the book collection with a specific title and published by a specific publisher.

    results = book_collection.find({'title': title, 'published_by': publisher})
    return results


def find_by_isbn(isbn):
    # Retrieves a book from the book collection based on the given ISBN.

    result = book_collection.find_one({'ISBN': isbn})
    return result


def insert_publisher(publisher):
    # Inserts a new publisher document into the publisher collection.

    result = publisher_collection.insert_one(publisher)
    return result.inserted_id


def insert_book(book):
    # Inserts a new book document into the book collection.

    result = book_collection.insert_one(book)
    return result.inserted_id


def update_book(isbn, updated_values):
    # Updates an existing book document in the book collection.

    result = book_collection.update_one({'ISBN': isbn}, {'$set': updated_values})
    return result.modified_count > 0


def delete_book(isbn):
    # Deletes an existing book document from the book collection.

    result = book_collection.delete_one({'ISBN': isbn})
    return result.deleted_count > 0
