from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='{}', fullname='{}', password='{}')>".format(self.name, self.fullname, self.password)


class Karma(Base):
    __tablename__ = 'karma'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    score = Column(Integer)
    last_vote = Column(String)

    def plus_karma(self):
        self.score += 1

    def min_karma(self):
        self.score -= 1

    def __repr__(self):
        return "<Karma(word='{}', score='{}')>".format(self.word, self.score)
