import json
import mock
import os

from django.test import TestCase

from dateme_app.controller import *
from dateme_app.tests.utils import *
from dateme_app.views import Status

class PersonControllerTests(TestCase):

    fixtures = ['test_cases.json']
    
    def setUp(self):

        # Load defaults provided by fixtures
        self.gender_male = load_gender_instance("Male")
        self.gender_female = load_gender_instance("Female")

        self.person_a = load_person_instance("Hector")
        self.person_b = load_person_instance("Carlita")

        # Load any custom fixtures. This should probably only be used if saving the fixtures
        # to the database is undesirable.
        base_dir = os.path.dirname(os.path.realpath(__file__))
        instances = create_fake_models_from_fixture(os.path.join(base_dir, '../fixtures', 'john.json'), save=False)
        self.person_new = instances[0]

    """
    Verify that get_person() returns the correct Person when given a valid username.
    """
    def test_get_person(self):

        # Test 1
        # Act: call controller
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person("Hector", status)
        
        # Assert: test return value
        self.assertEquals(status.errors, [])
        self.assertEquals(status.exceptions, [])
        self.assertTrue(status.success)
        self.assertEquals(status.data["person"], self.person_a)

        # Test 2
        # Act: call controller
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person(self.person_b.username, status)

        # Assert: test return value
        self.assertEquals(status.errors, [])
        self.assertEquals(status.exceptions, [])
        self.assertTrue(status.success)
        self.assertEquals(status.data["person"], self.person_b)

    """
    Verify that get_person() returns error 0202 when given the username of a non-existent person.
    """
    def test_get_person_non_existent(self):

        # Act: call controller
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person("Henry", status)

        # Assert: test return value
        self.assertEquals(status.errors[0][:4], "0202")
        self.assertEquals(status.exceptions, [])
        self.assertFalse(status.success)
        self.assertEquals(status.data, {})

    """
    Verify that get_person() returns error 0200 when given a username that matches more than one
    person in the database.
    """
    def test_get_person_multiple(self):

        # Arrange: write duplicate person to database
        person_a_copy = create_fake_person(self.person_a.username, self.person_a.gender, self.person_a.orientation)

        # Act: call controller
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person("Hector", status)
        
        # Assert: test return value
        self.assertEquals(status.errors[0][:4], "0200")
        self.assertEquals(status.exceptions, [])
        self.assertFalse(status.success)
        self.assertEquals(status.data, {})

    """
    Verify that register_person() inserts a new Person when given a valid username.
    """
    def test_register_person(self):

        # Arrange: build new person not yet in database
        new_person = self.person_new

        # Act: call controller
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = register_person(new_person, status)
        
        # Assert: test return value
        self.assertEquals(status.errors, [])
        self.assertEquals(status.exceptions, [])
        self.assertTrue(status.success)
        self.assertEquals(status.data["person"], new_person)

    """
    Verify that register_person() returns error 0201 when trying to register a username already
    in the database.
    """
    def test_register_person_multiple(self):

        # Act: call controller
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = register_person(self.person_a, status)

        # Assert: test return value
        self.assertEquals(status.errors[0][:4], "0201")
        self.assertEquals(status.exceptions, [])
        self.assertFalse(status.success)
        self.assertEquals(status.data, {})

    """
    Verify that update_person() updates an existing Person when given a valid username.
    """
    def test_update_person(self):

        # Arrange: update an existing person's information but do not save new information to database
        updated_person = create_fake_person(
            self.person_a.username, 
            self.person_a.gender, 
            self.person_a.orientation, 
            age_end=(self.person_a.age_end + 10), 
            save=False
        )

        # Act: call controller
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = update_person(updated_person, status)
        
        # Assert: test return value
        self.assertEquals(status.errors, [])
        self.assertEquals(status.exceptions, [])
        self.assertTrue(status.success)
        self.assertEquals(status.data["person"], updated_person)

    """
    Verify that update_person() returns error 0202 when given the username of a non-existent person.
    """
    def test_update_person_non_existent(self):

        # Arrange: update an unsaved person's information and do not save new information to database
        updated_person = self.person_new

        # Act: call controller
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = update_person(updated_person, status)
        
        # Assert: test return value
        self.assertEquals(status.errors[0][:4], "0202")
        self.assertEquals(status.exceptions, [])
        self.assertFalse(status.success)
        self.assertEquals(status.data, {})

    """
    Verify that update_person() returns error 0200 when given a username that matches more than one
    person in the database.
    """
    def test_update_person_multiple(self):

        # Arrange: write duplicate person to database
        updated_person = create_fake_person(self.person_a.username, self.person_a.gender, self.person_a.orientation)

        # Act: call controller
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = update_person(updated_person, status)
        
        # Assert: test return value
        self.assertEquals(status.errors[0][:4], "0200")
        self.assertEquals(status.exceptions, [])
        self.assertFalse(status.success)
        self.assertEquals(status.data, {})

class ServiceTests(TestCase):
    # TODO: Test cases for authenticate functions should go here.
    pass