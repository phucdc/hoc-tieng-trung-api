from models import Base
from schemas import *
from cruds import *
from database import engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List


Base.metadata.create_all(engine)
app = FastAPI(
    openapi_url="/openapi"
)


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
    return create_word(db, request)
    
    
@app.post("/words/import", response_model=List[WordSchema])
async def import_words_handler(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return import_words(db, file.file)
    
    
@app.get("/tabs/all", response_model=List[TabSchema])
async def get_all_tabs_handler(db: Session = Depends(get_db)):
    return get_all_tabs(db)


@app.get("/tabs/{tab_id}/get", response_model=TabSchema)
async def get_word_handler(tab_id: int, db: Session = Depends(get_db)):
    return get_tab(db, tab_id)
    
    
@app.post("/tabs/add", response_model=TabSchema)
async def add_tab(request: CreateTabRequest, db: Session = Depends(get_db)):
    return create_tab(db, request)


@app.delete("/tabs/{tab_id}/delete", response_model=TabSchema)
async def delete_tab_handler(tab_id: int, db: Session = Depends(get_db)):
    return delete_tab(db, tab_id)


@app.post("/tabs/{tab_id}/add", response_model=TabSchema)
async def add_words_to_tab_handler(tab_id: int, words: AddWordsToTabRequest, db: Session = Depends(get_db)):
    return add_words_to_tab(db, tab_id, words)
    