import certifi
import pymongo
from pymongo import MongoClient


def get_database():
    """
    Establishes a connection to the MongoDB database.

    Returns:
        Database: MongoDB database instance.
    """
    # Provide the MongoDB Atlas URL to connect Python to MongoDB using pymongo
    CONNECTION_STRING = "mongodb+srv://dron:12345@cluster0.re9rrdw.mongodb.net/fitnessAppUsers?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = pymongo.MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    # Create the database for our example (we will use the same database throughout the tutorial)
    return client['fitnessAppUsers']


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = get_database()