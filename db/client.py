from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Descomentar el db_client local o remoto correspondiente

# Base de datos local MongoDB
# db_client = MongoClient().local


uri = "mongodb+srv://test:test@incapas.xoneveu.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
db_client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    db_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
