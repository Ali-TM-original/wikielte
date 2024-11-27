import gridfs
from os import getenv
from asyncio import to_thread
from pymongo import AsyncMongoClient, MongoClient
from bson.objectid import ObjectId
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

    async def deleteFile(self, file_id: ObjectId):
        try:
            await to_thread(self.fs.delete, file_id)
            print(f"File with ID {file_id} successfully deleted.")
            return True
        except gridfs.errors.NoFile:
            print(f"No file found with ID {file_id}.")
            return False
        except Exception as e:
            print(f"Error deleting file with ID {file_id}: {e}")
            return False

    async def doesExist(self, r: ResourceModel):
        try:
            d = r.dict()
            cursor = self.db.resources.find({"name": d.get("name"),"course": d.get("course")})
            resources = await cursor.to_list(length=None)
            if not resources:
                return False
            return True
        except Exception as e:
            print(e)
            return False

    async def createResource(self, r: ResourceModel):
        d = r.dict()
        res = await self.getOne(d.get("name"), d.get("course"))
        if res:
            return False
        try:
            await self.db.resources.insert_one(d)
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
            res = await self.db.resources.find_one({"name": name, "course": course})
            return res  # This will return a dictionary or None
        except Exception as e:
            print(f"Error in getOne: {e}")
            return None

    async def deleteOne(self, name: str, course: str, creatorID: int):
        try:
            # Fetch the resource
            res = await self.getOne(name, course)
            if not res:
                print(f"Resource not found: {name} ({course})")
                return False  # Resource does not exist

            # Check if the creatorID matches
            if "creatorID" not in res or res["creatorID"] != creatorID:
                print(f"Permission denied for user {creatorID} to delete {name} ({course})")
                return False  # User is not authorized to delete this resource

            if res['fileID'] is not None:
                await self.deleteFile(ObjectId(res['fileID']))
            # Perform the deletion
            delete_result = await self.db.resources.delete_one({"name": name, "course": course})
            if delete_result.deleted_count > 0:
                print(f"Resource deleted: {name} ({course}) by user {creatorID}")
                return True
            else:
                print(f"Failed to delete resource: {name} ({course})")
                return False
        except Exception as e:
            print(f"Error in deleteOne: {e}")
            return False

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
