# File: app/schemas/group.py
from pydantic import BaseModel
from typing import List

class GroupBase(BaseModel):
    title: str
    creator_id: int

class GroupCreate(GroupBase):
    participant_ids: List[int]

class GroupResponse(GroupBase):
    id: int
    participant_ids: List[int]

    class Config:
        orm_mode = True
