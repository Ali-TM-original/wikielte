import gridfs
from os import getenv
from asyncio import to_thread
from pymongo import AsyncMongoClient, MongoClient
from .models import ResourceModel


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
        return {"data": file_data.read(), "name": file_data.filename}

    async def createResource(self, r: ResourceModel):
        try:
            await self.db.resources.insert_one(r.dict())
            return True
        except Exception as e:
            print(e)
            return False

    async def filterByCourse(self, course: str) -> bool:
        # Not Complete yet
        try:
            cursor = self.db.resources.find({"course": course})
            resources = await cursor.to_list(length=None)
            return resources
        except Exception as e:
            print(f"Error in filterByCourse: {e}")
            return False

    async def getOne(self, name: str, course: str):
        try:
            cursor = self.db.resources.find_one({"name": name, "course": course})
            res = await cursor.to_list(length=None)
            return res
        except Exception as e:
            print(f"Error in getOne {e}")
            return []

    async def getAllResources(self) -> list[dict]:
        """
        Fetch all resources from the database.
        """
        try:
            cursor = self.db.resources.find()  # Retrieve all documents
            resources = await cursor.to_list(length=None)  # Convert cursor to a list
            return resources
        except Exception as e:
            print(f"Error in getAllResources: {e}")
            return []
