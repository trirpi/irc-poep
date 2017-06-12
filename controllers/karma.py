from controllers.orm.models import Karma
from controllers.orm import session


def get_karma(word):
    item = session.query(Karma).filter_by(word=word).first()
    return "karma van " + word + " is " + str(item.score)


def add_karma_item(word):
    item = session.query(Karma).filter_by(word=word).first()
    if not item:
        new_word = Karma(word=word, score=0)
        session.add(new_word)
        session.commit()
        return word + " added"
    else:
        return word + "allready in dict"


def increment_karma(word, username):
    item = session.query(Karma).filter_by(word=word).first()
    item.plus_karma()
    item.last_vote = username
    return "karma van " + word + " is nu " + str(item.score)


def decrement_karma(word, username):
    item = session.query(Karma).filter_by(word=word).first()
    item.min_karma()
    item.last_vote = username
    return "karma van " + word + " is nu " + str(item.score)
