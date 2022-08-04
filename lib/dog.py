from sqlalchemy import create_engine

from lib.models import Dog

engine = create_engine('sqlite:///:memory:')

def create_table(base):
    base.metadata.create_all(engine)
    return engine

def save(session, dog):
    session.add(dog)
    session.commit()
    return session

def new_from_db(session):
    return session.query(Dog).first()

def get_all(session):
    return [dog for dog in session.query(Dog)]

def find_by_name(session, name):
    return session.query(Dog).filter_by(dog_name=name).first()

def find_by_id(session, id):
    return session.query(Dog).filter_by(dog_id=id).first()

def find_by_name_and_breed(session, name, breed):
    return session.query(Dog).filter_by(dog_name=name, dog_breed=breed).first()

def update(session, dog):
    session.commit()
