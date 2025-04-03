from pydantic import BaseModel
from typing import List, Optional

class GroupBase(BaseModel):
    title: str
    creator_id: int

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    
    class Config:
        from_attributes = True

class GroupWithParticipants(Group):
    participants: List[int] = []
    
    class Config:
        from_attributes = True