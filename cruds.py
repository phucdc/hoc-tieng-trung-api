from sqlalchemy.orm import Session
from schemas import *
from models import Word, Tab
from ultilities import get_voice


def get_all_words(db: Session):
    return db.query(Word).all()


def get_word(db: Session, word_id: int):
    return db.query(Word).filter_by(id=word_id).first()


def create_word(db: Session, word: CreateWordRequest):
    if db.query(Word).filter_by(chinese=word.chinese).first():
        return
    voice = get_voice(word.chinese)
    db_word = Word(chinese=word.chinese, pinyin=word.pinyin, meaning=word.meaning, voice=voice)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word
    