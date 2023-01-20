from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:')

def create_table(base):
    pass

def save(session, dog):
    pass

def new_from_db(session):
    pass

def get_all(session):
    pass

def find_by_name(session, name):
    pass

def find_by_id(session, id):
    pass

def find_by_name_and_breed(session, name, breed):
    pass

def update_breed(session, dog, breed):
    pass