from os import getenv
from asyncio import to_thread
from pymongo import AsyncMongoClient, MongoClient
import gridfs


class DatabaseClient:
    def __init__(self):
        if getenv("DATABASEURI") and getenv("DBPORT"):
            self.client = AsyncMongoClient(getenv("DATABASEURI"), port=int(getenv("DBPORT")))
            self.sClient = MongoClient(getenv("DATABASEURI"), port=int(getenv("DBPORT")))
        else:
            self.client = AsyncMongoClient()
            self.sClient = MongoClient()
        self.db = self.client.get_database("elte_resourses")
        self.fs = gridfs.GridFS(self.sClient.get_database("elte_resourses"))
        print("DATABASE CONNECTED")

    async def uploadFile(self, fb: bytes, filename: dict[str, any]):
        file_id = await to_thread(self.fs.put, fb, filename=filename)
        return file_id

    async def getFile(self, id):
        file_data = await to_thread(self.fs.get, id)  # Retrieve the file
        return {"data":file_data.read(), "name":file_data.filename}
