import datetime

from django.core import serializers
from django.utils import timezone
from dateme_app.models import Person, Gender

def create_fake_gender(gender, save=True):

    """
    Create a Gender instance. Default save to database.
    """

    g = Gender(name=gender)
    if save:
        g.save()
    return g

def create_fake_person(username, gender, orientation, handle=None, token="Fake token", token_expiration=None, tagline="Fake tagline",
                        birthday=None, age_start=18, age_end=50, age=116, save=True):
    
    """
    Create a Person instance. Default save to database.
    """

    if not handle:
        handle=username

    if not birthday:
        birthday = datetime.date(1900, 01, 01)

    if not token_expiration:
        token_expiration = timezone.now() + datetime.timedelta(days=1)

    p = Person(
        username=username,
        handle=handle, 
        token=token,
        token_expiration=token_expiration,
        tagline=tagline,
        birthday=birthday,
        age_start=age_start,
        age_end=age_end,
        gender=gender,
        orientation=orientation,
        age=age
    )

    if save:
        p.save()
    return p
	
def create_fake_models_from_fixture(fixture, type="json", save=True):

    """
    Return a list of Model objects instantiated from a fixture. By default, the 
    fixture is assumed to be json and the objects are saved to the database.
    """

    model_instances = []

    with open(fixture, 'r') as f:
        data = f.read()
        for deserialized_object in serializers.deserialize(type, data):
            if save:
                deserialized_object.save()
            model_instances.append(deserialized_object.object)

    return model_instances

def load_gender_instance(gender):

    """
    Return a Gender instance from the database based on name.
    """

    g = Gender.objects.get(name=gender)
    return g

def load_person_instance(username):

    """
    Return a Gender instance from the database based on username.
    """
    
    p = Person.objects.get(username=username)
    return p