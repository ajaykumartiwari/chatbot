
# try:
#     from urlparse import urlparse
# except ImportError:
#     from urllib.parse import urlparse

from pymongo import MongoClient


""" Database connection """
client = MongoClient('localhost', 27017)
db = client.chatbot
conn = db.bankFaq
# from pymongo.errors import ConnectionFailure

# class Connection(object):

#     _instance = None
#     connection = None
#     _database = None


#     @classmethod
#     def instance(cls):
#         """ Retrieves the shared connection. """
#         if not cls._instance:
#             cls._instance = Connection()
#         return cls._instance
    
#     @classmethod
#     def connect(cls, database=None, uri="mongodb://localhost:27017", **kwargs):
#         if not database:
#             database = urlparse(uri).path
#             while database.statrtwith("/"):
#                 database = database[1:]
#             if not database:
#                 raise ValueError("A database name is required to connect.")
    
#         conn = cls.instance()
#         conn._database = database
#         conn.connection = MongoClient(uri, **kwargs)
#         return conn.connection

#     def get_database(self, database=None):
#         """ Retrieves a database from an existing connection. """
#         if not self.connection:
#             raise ConnectionFailure('No connection')
#         if not database:
#             if not self._database:
#                 raise Exception('No database submitted')
#             database = self._database
#         return self.connection[database]

#     def get_collection(self, collection, database=None):
#         """ Retrieve a collection from an existing connection. """
#         return self.get_database(database=database)[collection]


# class Session(object):
#     """ This class just wraps a connection instance """

#     def __init__(self, database, *args, **kwargs):
#         """ Stores a connection instance """
#         self.connection = None
#         self.database = database
#         self.args = args
#         self.kwargs = kwargs

#     def connect(self):
#         """ Connect to MongoDB """
#         connection = Connection()
#         connection._database = self.database
#         connection.connection = MongoClient(*self.args, **self.kwargs)
#         self.connection = connection

#     def disconnect(self):
#         # PyMongo removed the disconnect keyword, close() is now used.
#         self.close()

#     def close(self):
#         self.connection.connection.close()

#     def __enter__(self):
#         """ Open the connection """
#         self.connect()
#         return self

#     def __exit__(self, type, value, traceback):
#         """ Close the connection """
#         self.disconnect()


# def connect(*args, **kwargs):
#     """
#     Initializes a connection and the database. It returns
#     the pymongo connection object so that end_request, etc.
#     can be called if necessary.
#     """
#     return Connection.connect(*args, **kwargs)


# def session(database, *args, **kwargs):
#     """
#     Returns a session object to be used with the `with` statement.
#     """
#     return Session(database, *args, **kwargs)