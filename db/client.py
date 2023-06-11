from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Descomentar el db_client local o remoto correspondiente

# Base de datos local MongoDB
db_client = MongoClient().local


# uri = "mongodb+srv://aatn1321:rgFCNhw7hhvkN5ad@incapas.xoneveu.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
# db_client = MongoClient(uri, server_api=ServerApi('1')).test
