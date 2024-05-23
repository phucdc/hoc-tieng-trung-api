from models import Base
from schemas import *
from cruds import *
from database import engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List


Base.metadata.create_all(engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/words/all", response_model=List[WordSchema])
async def all_words(db: Session = Depends(get_db)):
    return get_all_words(db)
    
    
@app.get("/words/{word_id}/get", response_model=WordSchema)
async def get_word_by_id(word_id: int, db: Session = Depends(get_db)):
    return get_word(db, word_id)
    

@app.post("/words/add", response_model=WordSchema)
async def add_word(request: CreateWordRequest, db: Session = Depends(get_db)):
    db_word = create_word(db, request)
    if not db_word:
        raise HTTPException(status_code=400, detail='[Add_Word] error when trying to add new word')
    return db_word
    
    
@app.post("/words/import", response_model=List[WordSchema])
async def import_word(file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    ...