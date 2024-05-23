from sqlalchemy.orm import Session
from schemas import *
from models import Word, Tab, associations
from ultilities import get_voice, words_from_excel


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
    
    
def import_words(db: Session, file):
    words = words_from_excel(file)
    db_words = []
    for word in words:
        chinese, pinyin, meaning = word
        db_word = Word(chinese=chinese, pinyin=pinyin, meaning=meaning)
        db_words.append(create_word(db, db_word))
    return db_words


def get_all_tabs(db: Session):
    return db.query(Tab).all()


def get_tab(db: Session, tab_id: int):
    return db.query(Tab).filter_by(id=tab_id).first()


def create_tab(db: Session, tab: CreateTabRequest):
    if db.query(Tab).filter_by(name=tab.name).first():
        return
    db_tab = Tab(name=tab.name)
    db.add(db_tab)
    db.commit()
    db.refresh(db_tab)
    return db_tab


def delete_tab(db: Session, tab_id: int):
    db_tab = get_tab(db, tab_id)
    if not db_tab:
        return
    db_tab.remove_associations(db)
    db.delete(db_tab)
    db.commit()
    return db_tab


def add_words_to_tab(db: Session, tab_id: int, words: AddWordsToTabRequest):
    db_tab = get_tab(db, tab_id)
    if not db_tab:
        return
    for word_id in words.words:
        db_word = get_word(db, word_id)
        db_tab.words.append(db_word)
    db.commit()
    db.refresh(db_tab)
    return db_tab
