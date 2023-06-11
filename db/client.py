from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Descomentar el db_client local o remoto correspondiente

# Base de datos local MongoDB
db_client = MongoClient().local



# Create a new client and connect to the server
# db_client = MongoClient(uri, server_api=ServerApi('1')).test
