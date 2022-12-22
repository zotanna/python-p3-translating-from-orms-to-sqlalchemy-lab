from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from dog import (
    create_table,
    find_by_id,
    find_by_name,
    find_by_name_and_breed,
    save,
    new_from_db,
    get_all,
    update_breed
)
from models import Base, Dog

class TestModels:
    '''app/models.py'''

    def test_has_name_and_breed_attributes(self):
        '''contains model "Dog" with name and breed attributes.'''
        dog = Dog(name="joey", breed="cocker spaniel")
        assert(dog.name == "joey" and dog.breed == "cocker spaniel")

class TestDog:
    '''app/dog.py'''


    def test_creates_table(self):
        '''contains function "create_table()" that takes a declarative_base, creates table "dogs" if it does not exist, and returns the engine.'''
        engine = create_table(Base)
        assert(engine != None)

    def test_saves_dog(self):
        '''contains function "save()" that takes a Dog instance and session as arguments, saves the dog to the database, and returns the session.'''
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

        Session = sessionmaker(engine)
        session = Session()

        joey = Dog(name="joey", breed="cocker spaniel")
        save(session, joey)

        Session = sessionmaker(engine)
        test_session = Session()

        db_dog = test_session.query(Dog).first()
        assert(db_dog.name ==  'joey' and db_dog.breed == 'cocker spaniel')

    def test_returns_new_instance_from_db(self):
        '''contains function "new_from_db()" that takes a database row and returns a Dog instance.'''
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        session = Session()
        new_dog = Dog(name="joey", breed="cocker spaniel")
        session.add(new_dog)
        session.commit()
        dog = new_from_db(session, session.query(Dog).first())
        assert(hasattr(dog, 'id') and hasattr(dog, 'name') and hasattr(dog, 'breed'))

    def test_gets_all(self):
        '''contains function "get_all()" that takes a session and returns a list of Dog instances for every record in the database.'''
        # add new dogs
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

        Session = sessionmaker(engine)
        session = Session()

        dog_2 = Dog(name="fanny", breed="cockapoo")
        dog_3 = Dog(name="conan", breed="chihuahua")
        session.bulk_save_objects([dog_2, dog_3])
        session.commit()

        all_dogs = get_all(session)
        assert(all_dogs[0].name == 'fanny' and \
                all_dogs[1].name == 'conan')


    def test_finds_by_name(self):
        '''contains function "find_by_name()" that takes a session and name and returns a Dog instance corresponding to its database record retrieved by name.'''
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

        Session = sessionmaker(engine)
        session = Session()
        dog = Dog(name="conan", breed="chihuahua")
        session.add(dog)
        session.commit()
        conan = find_by_name(session, 'conan')
        assert(conan.name == 'conan')

    def test_finds_by_id(self):
        '''contains function "find_by_id()" that takes a session and id and returns a Dog instance corresponding to its database record retrieved by id.'''
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

        Session = sessionmaker(engine)
        session = Session()
        dog = Dog(name="conan", breed="chihuahua")
        session.add(dog)
        session.commit()
        
        dog_1 = find_by_id(session, 1)
        assert(dog_1.id == 1)

    def test_finds_by_name_and_breed(self):
        '''contains function "find_by_name_and_breed()" that takes a session, a name, and a breed as arguments and returns a Dog instance matching that record.'''
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

        Session = sessionmaker(engine)
        session = Session() 
        dog = Dog(name="fanny", breed="cockapoo")
        session.add(dog)
        session.commit()
        
        fanny = find_by_name_and_breed(session, 'fanny', 'cockapoo')
        assert(fanny.name == 'fanny' and fanny.breed == 'cockapoo')
    def test_updates_record(self):
        '''contains function "update_breed()" that takes a session instance, and breed as arguments and updates the instance's breed.'''
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        session = Session() 
        dog = Dog(name="joey", breed="cocker spaniel")
        session.add(dog)
        session.commit()

        joey = session.query(Dog).filter_by(name='joey').first()
        update_breed(session, joey, 'bulldog')
        updated_record = session.query(Dog).filter_by(name='joey').first()
        assert(updated_record.breed == 'bulldog')
