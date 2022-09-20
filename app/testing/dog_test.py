from sqlalchemy.orm import sessionmaker

from dog import (
    create_table,
    find_by_id,
    find_by_name,
    find_by_name_and_breed,
    save,
    new_from_db,
    get_all,
    update
)
from models import Base, Dog

class TestDog:
    '''app/dog.py'''

    engine = create_table(Base)
    Session = sessionmaker(engine)
    session = Session()

    def test_creates_table(self):
        '''contains function "create_table()" that takes a declarative_base, creates table "dogs" if it does not exist, and returns the engine.'''
        engine = create_table(Base)
        Session = sessionmaker(engine)
        session = Session()
        assert(session.query(Dog))

    def test_saves_dog(self):
        '''contains function "save()" that takes a Dog instance and session as arguments, saves the dog to the database, and returns the session.'''
        joey = Dog(name="joey", breed="cocker spaniel")
        session = save(TestDog.session, joey)
        db_dog = session.query(Dog).first()
        assert(db_dog.name ==  'joey' and db_dog.breed == 'cocker spaniel')

    def test_creates_new_instance_from_db(self):
        '''contains function "new_from_db()" that takes a database row and creates and returns a Dog instance.'''
        dog = new_from_db(TestDog.session)
        assert(hasattr(dog, 'id') and hasattr(dog, 'name') and hasattr(dog, 'breed'))

    def test_gets_all(self):
        '''contains function "get_all()" that takes a session and returns a list of Dog instances for every record in the database.'''
        # add new dogs
        dog_2 = Dog(name="fanny", breed="cockapoo")
        dog_3 = Dog(name="conan", breed="chihuahua")
        TestDog.session.bulk_save_objects([dog_2, dog_3])
        TestDog.session.commit()

        all_dogs = get_all(TestDog.session)
        assert(all_dogs[0].name == 'joey' and \
            all_dogs[1].name == 'fanny' and \
            all_dogs[2].name == 'conan')


    def test_finds_by_name(self):
        '''contains function "find_by_name()" that takes a session and name and returns a Dog instance corresponding to its database record retrieved by name.'''
        conan = find_by_name(TestDog.session, 'conan')
        assert(conan.name == 'conan')

    def test_finds_by_id(self):
        '''contains function "find_by_id()" that takes a session and id and returns a Dog instance corresponding to its database record retrieved by id.'''
        dog_1 = find_by_id(TestDog.session, 1)
        assert(dog_1.id == 1)

    def test_finds_by_name_and_breed(self):
        '''contains function "find_by_name_and_breed()" that takes a session, a name, and a breed as arguments and returns a Dog instance matching that record.'''
        fanny = find_by_name_and_breed(TestDog.session, 'fanny', 'cockapoo')
        assert(fanny.name == 'fanny' and fanny.breed == 'cockapoo')
    
    def test_updates_record(self):
        '''contains function "update()" that takes a session and instance as arguments and updates the instance's corresponding database record to match its new attribute values.'''
        joey = TestDog.session.query(Dog).filter_by(name='joey').first()
        joey.breed = 'bulldog'
        update(TestDog.session, joey)
        updated_record = TestDog.session.query(Dog).filter_by(name='joey').first()
        assert(updated_record.breed == 'bulldog')
