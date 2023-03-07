import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from dog import (
    create_table,
    find_by_id,
    find_by_name,
    find_by_name_and_breed,
    save,
    get_all,
    update_breed
)
from models import Base, Dog
from testing.conftest import db_dir, SQLITE_URL

class TestModels:
    '''lib/models.py'''

    def test_has_name_and_breed_attributes(self):
        '''contains model "Dog" with name and breed attributes.'''
        dog = Dog(name="joey", breed="cocker spaniel")
        assert(dog.name == "joey" and dog.breed == "cocker spaniel")

class TestDog:
    '''lib/dog.py'''

    def test_creates_table(self):
        '''contains function "create_table()" that takes a declarative_base and creates a SQLite database.'''
        
        engine = create_engine(SQLITE_URL)
        create_table(Base, engine)
        assert os.path.exists(db_dir)
        os.remove(db_dir)

    def test_saves_dog(self):
        '''contains function "save()" that takes a Dog instance as an argument and saves the dog to the database.'''

        engine = create_engine(SQLITE_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        joey = Dog(name="joey", breed="cocker spaniel")
        save(session, joey)

        assert session.query(Dog).first().name == 'joey'
        assert session.query(Dog).first().breed == 'cocker spaniel'

        os.remove(db_dir)

    def test_gets_all(self):
        '''contains function "get_all()" that takes a session and returns a list of Dog instances for every record in the database.'''

        engine = create_engine(SQLITE_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        session = Session()

        dog_1 = Dog(name="fanny", breed="cockapoo")
        dog_2 = Dog(name="conan", breed="chihuahua")
        session.add_all([dog_1, dog_2])
        session.commit()

        all_dogs = get_all(session)
        assert all_dogs[0].name == 'fanny' and \
                all_dogs[1].name == 'conan'
        
        session.query(Dog).delete()
        session.commit()
        os.remove(db_dir)


    def test_finds_by_name(self):
        '''contains function "find_by_name()" that takes a session and name and returns a Dog instance corresponding to its database record retrieved by name.'''
        
        engine = create_engine(SQLITE_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        session = Session()
        
        dog = Dog(name="conan", breed="chihuahua")
        session.add(dog)
        session.commit()
        
        conan = find_by_name(session, 'conan')
        assert(conan.name == 'conan')

        os.remove(db_dir)

    def test_finds_by_id(self):
        '''contains function "find_by_id()" that takes a session and id and returns a Dog instance corresponding to its database record retrieved by id.'''
        
        engine = create_engine(SQLITE_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        session = Session()

        dog = Dog(name="conan", breed="chihuahua")
        session.add(dog)
        session.commit()
        
        dog_1 = find_by_id(session, dog.id)
        assert dog_1.id == dog.id
        assert dog_1.name == 'conan'
        assert dog_1.breed == 'chihuahua'

        os.remove(db_dir)

    def test_finds_by_name_and_breed(self):
        '''contains function "find_by_name_and_breed()" that takes a session, a name, and a breed as arguments and returns a Dog instance matching that record.'''
        
        engine = create_engine(SQLITE_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        session = Session() 
        
        dog = Dog(name="fanny", breed="cockapoo")
        session.add(dog)
        session.commit()
        
        fanny = find_by_name_and_breed(session, 'fanny', 'cockapoo')
        assert fanny.name == 'fanny' and fanny.breed == 'cockapoo'

        os.remove(db_dir)

    def test_updates_record(self):
        '''contains function "update_breed()" that takes a session instance, and breed as arguments and updates the instance's breed.'''
        
        engine = create_engine(SQLITE_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        session = Session() 
        
        dog = Dog(name="joey", breed="cocker spaniel")
        session.add(dog)
        session.commit()

        joey = session.query(Dog).filter_by(name='joey').first()
        update_breed(session, joey, 'bulldog')
        updated_record = session.query(Dog).filter_by(name='joey').first()
        
        assert updated_record.breed == 'bulldog'
        
        os.remove(db_dir)
