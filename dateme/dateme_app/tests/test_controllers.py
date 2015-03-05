import json
import mock

from django.test import TestCase

from dateme_app.controller import *
from dateme_app.tests.utils import create_fake_gender, create_fake_person
from dateme_app.views import Status

class PersonControllerTests(TestCase):
    def setUp(self):
        self.gender_male = create_fake_gender("male")
        self.gender_female = create_fake_gender("female")

        self.person_a = create_fake_person("Hector", self.gender_male, self.gender_female)
        self.person_b = create_fake_person("Carlita", self.gender_female, self.gender_male)

    """
    Verify that get_person() returns the correct Person when given a valid username.
    """
    def test_get_person(self):
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person("Hector", status)
        self.assertEquals(status.errors, [])
        self.assertTrue(status.success)
        self.assertEquals(status.data["person"], self.person_a)

        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person(self.person_b.username, Status())
        self.assertEquals(status.errors, [])
        self.assertEquals(status.exceptions, [])
        self.assertTrue(status.success)
        self.assertEquals(status.data["person"], self.person_b)

    """
    Verify that get_person() returns error 0202 when given the username of a non-existent person.
    """
    def test_get_person_non_existent(self):
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person("Henry", status)
        self.assertEquals(status.errors[0][:4], "0202")
        self.assertEquals(status.exceptions, [])
        self.assertFalse(status.success)
        self.assertEquals(status.data, {})

    """
    Verify that get_person() returns error 0200 when given a username that matches more than one
    person in the database.
    """
    def test_get_person_multiple(self):
        person_a_copy = create_fake_person("Hector", self.gender_male, self.gender_female)

        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person("Hector", status)
        self.assertEquals(status.errors[0][:4], "0200")
        self.assertEquals(status.exceptions, [])
        self.assertFalse(status.success)
        self.assertEquals(status.data, {})

    """
    Verify that register_person() inserts a new Person when given a valid username.
    """
    def test_register_person(self):
        person = create_fake_person("John", self.gender_male, self.gender_female, save=False)

        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = register_person(person, status)
        self.assertEquals(status.errors, [])
        self.assertEquals(status.exceptions, [])
        self.assertTrue(status.success)
        self.assertEquals(status.data["person"], person)

    """
    Verify that register_person() returns error 0201 when trying to register a username already
    in the database.
    """
    def test_register_person_multiple(self):
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = register_person(self.person_a, status)
        self.assertEquals(status.errors[0][:4], "0201")
        self.assertEquals(status.exceptions, [])
        self.assertFalse(status.success)
        self.assertEquals(status.data, {})

    """
    Verify that update_person() updates an existing Person when given a valid username.
    """
    def test_update_person(self):
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        updated_person = create_fake_person("Hector", self.gender_male, self.gender_female, age_end=25, save=False)
        status = update_person(updated_person, status)
        self.assertEquals(status.errors, [])
        self.assertEquals(status.exceptions, [])
        self.assertTrue(status.success)
        self.assertEquals(status.data["person"], updated_person)

    """
    Verify that update_person() returns error 0202 when given the username of a non-existent person.
    """
    def test_update_person_non_existent(self):
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        updated_person = create_fake_person("Jeremy", self.gender_male, self.gender_female, age_end=25, save=False)
        status = update_person(updated_person, status)
        self.assertEquals(status.errors[0][:4], "0202")
        self.assertEquals(status.exceptions, [])
        self.assertFalse(status.success)
        self.assertEquals(status.data, {})

    """
    Verify that update_person() returns error 0200 when given a username that matches more than one
    person in the database.
    """
    def test_update_person_multiple(self):
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        updated_person = create_fake_person("Hector", self.gender_male, self.gender_female, age_end=25)
        status = update_person(updated_person, status)
        self.assertEquals(status.errors[0][:4], "0200")
        self.assertEquals(status.exceptions, [])
        self.assertFalse(status.success)
        self.assertEquals(status.data, {})

class ServiceTests(TestCase):
    # TODO: Test cases for authenticate methods should go here.
    pass