from lib.models import Dog

class TestModels:
    '''lib/models.py'''

    def test_has_name_and_breed_attributes(self):
        '''contains model "Dog" with dog_name and dog_breed attributes.'''
        dog = Dog(dog_name="joey", dog_breed="cocker spaniel")
        assert(dog.dog_name == "joey" and dog.dog_breed == "cocker spaniel")
