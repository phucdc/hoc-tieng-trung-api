from pydantic import BaseModel
from typing import List
    

class WordSchema(BaseModel):
    id: int
    chinese: str
    pinyin: str
    meaning: str
    voice: str
    
    class Config:
        orm_mode = True


class TabSchema(BaseModel):
    id: int
    name: str
    words: List[WordSchema]
    
    class Config:
        orm_mode = True


class CreateWordRequest(BaseModel):
    chinese: str
    pinyin: str
    meaning: str
    
    
class CreateTabRequest(BaseModel):
    name: str
    
    
class AddWordsToTabRequest(BaseModel):
    words: List[int]
