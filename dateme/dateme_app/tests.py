import json
import mock

from django.test import TestCase
from rest_framework.test import APITestCase

from dateme_app.controller import get_person
from dateme_app.messages import get_error_message
from dateme_app.models import Person
from dateme_app.serializers import PersonSerializer
from dateme_app.test.utils import create_fake_gender, create_fake_person
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
        self.assertTrue(status.success)
        self.assertEquals(status.data["person"], self.person_b)

    """
    Verify that get_person() returns error 0202 when given the username of a non-existent person.
    """
    def test_get_person_non_existent(self):
        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person("Henry", status)
        self.assertEquals(status.errors[0][:4], "0202")
        self.assertFalse(status.success)
        self.assertEquals(status.data["person"], {})

    """
    Verify that get_person() returns error 0200 when given a username that matches more than one
    person in the database.
    """
    def test_get_person_multiple(self):
        person_a_copy = create_fake_person("Hector", self.gender_male, self.gender_female)

        status = Status(success=False, data={}, exceptions=[], errors=[], status_code=403)
        status = get_person("Hector", status)
        self.assertEquals(status.errors[0][:4], "0200")
        self.assertFalse(status.success)
        self.assertEquals(status.data["person"], {})


class PersonAPITests(APITestCase):
    def setUp(self):
        self.gender_male = create_fake_gender("male")
        self.gender_female = create_fake_gender("female")

        self.person_a = create_fake_person("Hector", self.gender_male, self.gender_female)

        self.url = '/dateme_app/get_person/' # replace this with reverse(<url_name>)
        self.data = {'app':
                    {
                        'key': 'qahLbKqZG79E4N9XJV9nfdsj'
                    },
                'person':
                    {
                        'username': self.person_a.username,
                        'token': self.person_a.token
                    }
                }

    """
    Verify that the get_person() view returns a valid 200 response when given a valid request.
    """
    @mock.patch('dateme_app.controller.get_person')
    @mock.patch('dateme_app.views.login')
    def test_get_person_view(self, mock_login, mock_get_person):
        status = Status(success=True, data={}, exceptions=[], errors=[], status_code=200)
        mock_login.return_value = status

        status = Status(success=True, data={"person":self.person_a}, exceptions=[], errors=[], status_code=200)
        mock_get_person.return_value = status

        response = self.client.post(self.url, self.data, format='json')
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json["success"])
        self.assertEqual(response_json["exceptions"], [])
        self.assertEqual(response_json["errors"], [])
        self.assertEqual(response_json["data"], {"person": dict(PersonSerializer(self.person_a).data)})

    """
    Verify that the get_person() view returns a 500 response when an unexpected exception occurs.
    """
    @mock.patch('dateme_app.controller.get_person')
    @mock.patch('dateme_app.views.login')
    def test_get_person_view_exception(self, mock_login, mock_get_person):
        status = Status(success=True, data={}, exceptions=[], errors=[], status_code=200)
        mock_login.return_value = status

        mock_get_person.side_effect = Exception("Exception thrown by get_person()")

        response = self.client.post(self.url, self.data, format='json')
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, 500)
        self.assertFalse(response_json["success"])
        self.assertEqual(response_json["exceptions"], ["Exception thrown by get_person()"])
        self.assertEqual(response_json["errors"], [])
        self.assertEqual(response_json["data"], {})