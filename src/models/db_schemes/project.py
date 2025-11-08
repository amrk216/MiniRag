from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field (None , alias = '_id')
    project_id: str = Field(default=..., min_length=1)

    @validator ('project_id')
    def validate_project_id(cls,value):
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return value
    

    class Config:
        arbitrary_types_allowed = True


    @classmethod
    def get_indexes(cls):
        return [
            {
                'key': [

                    ("project_id",1 ) #? MongoDB will index all documents by project_id in ascending = 1 order 
                ],
                'name': "project_id_index_1", 
                "unique": True
            }
        ]