from models import Dog

class TestModels:
    '''app/models.py'''

    def test_has_name_and_breed_attributes(self):
        '''contains model "Dog" with name and breed attributes.'''
        dog = Dog(name="joey", breed="cocker spaniel")
        assert(dog.name == "joey" and dog.breed == "cocker spaniel")
