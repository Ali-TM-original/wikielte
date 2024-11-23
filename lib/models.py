from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from bson.objectid import ObjectId


class ResourceModel(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id", default=None)
    name: str
    course: str
    description: str
    creatorID: int
    creatorName: str
    fileID: Optional[ObjectId] = None  # References the file in GridFS
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Ada Entry",
                "course": "Ada",
                "description": "This resource is a link to Ada resources",
                "creatorID": 12345,
                "creatorName": "AliDaOriginal",
                "fileID": "64afdc2b9e3f2b73193a3f1d"  # Optional GridFS file ID
            }
        },
    )
