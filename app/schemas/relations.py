from pydantic import BaseModel
from typing import List

class UserWithGroups(BaseModel):
    id: int
    name: str
    email: str
    groups: List[int] = []
    
    class Config:
        from_attributes = True

class ChatWithMessages(BaseModel):
    id: int
    title: Optional[str]
    messages: List[str] = []
    
    class Config:
        from_attributes = True