from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Karma, Base

engine = create_engine('sqlite:///controllers/orm/data.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
