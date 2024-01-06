import pymongo

# pymongo_connector.py
# Modified By: Ben Blake

# This module establishes a connection to a MongoDB database and initializes collections for book and publisher
# management.

dbname = 'bookmanager'

book_collection = 'Book'
publisher_collection = 'Publisher'

client = pymongo.MongoClient('mongodb://root:password@127.0.0.1:27017/')

mydb = client[dbname]

book_collection = mydb[book_collection]
publisher_collection = mydb[publisher_collection]
