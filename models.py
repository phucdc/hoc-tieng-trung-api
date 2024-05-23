from database import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


associations = Table(
    'associations',
    Base.metadata,
    Column('word_id', ForeignKey('words.id'), primary_key=True),
    Column('tab_id', ForeignKey('tabs.id'), primary_key=True)
)


class Word(Base):
    __tablename__ = 'words'
    
    id = Column(Integer, primary_key=True)
    chinese = Column(String, unique=True, nullable=False)
    pinyin = Column(String, nullable=False)
    meaning = Column(String, nullable=False)
    voice = Column(String, nullable=False)
    
    tabs = relationship('Tab', secondary='associations', back_populates='words')
    
    
class Tab(Base):
    __tablename__ = 'tabs'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    words = relationship('Word', secondary='associations', back_populates='tabs')
    
    def remove_associations(self, session):
        """
        Remove associations between this Tab and its associated Word instances.
        """
        associated_words = session.query(Word).join(associations).filter(
            associations.c.tab_id == self.id
        ).all()

        for word in associated_words:
            self.words.remove(word)

        session.commit()
