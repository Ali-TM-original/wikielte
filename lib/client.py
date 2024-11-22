from os import getenv
from pymongo import AsyncMongoClient


class DatabaseClient:
    def __init__(self):
        if getenv("DATABASEURI") and getenv("DBPORT"):
            self.client = AsyncMongoClient(getenv("DATABASEURI"), port=int(getenv("DBPORT")))
        else:
            self.client = AsyncMongoClient(getenv("DATABASEURI"))