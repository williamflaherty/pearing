import json
import mock
import os

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from dateme_app.serializers import *
from dateme_app.tests.utils import *
from dateme_app.views import Status

class PearingTestCase(APITestCase):

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

    def build_data(self, app=True, *args, **kwargs):
        data = {}

        if app:
            data["app"] = {'key': 'qahLbKqZG79E4N9XJV9nfdsj'}

        for key, value in kwargs.items():
            data[key] = value

        return data

class PersonAPITests(PearingTestCase):

    """
    Verify that the get_person() view returns a valid 200 response when given a valid request.
    """
    @mock.patch('dateme_app.controller.get_person')
    @mock.patch('dateme_app.views.login')
    def test_get_person_view(self, mock_login, mock_get_person):

        # Arrange: mock dependencies
        status = Status(success=True, data={}, exceptions=[], errors=[], status_code=200)
        mock_login.return_value = status

        # mock the database returning an existing person
        status = Status(success=True, data={"person":self.person_a}, exceptions=[], errors=[], status_code=200)
        mock_get_person.return_value = status

        # Act: call view
        url = reverse('dateme_app:get_person')
        request_data = self.build_data(person=PersonSerializer(self.person_a, fields=['username', 'token']).data)
        response = self.client.post(url, request_data, format='json')
        response_json = json.loads(response.content)

        # Assert: test response
        response_data = self.build_data(app=False, person=PersonSerializer(self.person_a).data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json["success"])
        self.assertEqual(response_json["exceptions"], [])
        self.assertEqual(response_json["errors"], [])
        self.assertEqual(response_json["data"], response_data)

    """
    Verify that the get_person() view returns a 500 response when an unexpected exception occurs.
    """
    @mock.patch('dateme_app.controller.get_person')
    @mock.patch('dateme_app.views.login')
    def test_get_person_view_exception(self, mock_login, mock_get_person):

        # Arrange: mock dependencies
        status = Status(success=True, data={}, exceptions=[], errors=[], status_code=200)
        mock_login.return_value = status

        # mock the view generating an exception
        exception_message = "Exception thrown by get_person()"
        mock_get_person.side_effect = Exception(exception_message)
        
        # Act: call view
        url = reverse('dateme_app:get_person')
        request_data = self.build_data(person=PersonSerializer(self.person_a, fields=('username', 'token')).data)
        response = self.client.post(url, request_data, format='json')
        response_json = json.loads(response.content)

        # Assert: test response
        self.assertEqual(response.status_code, 500)
        self.assertFalse(response_json["success"])
        self.assertEqual(response_json["exceptions"], [exception_message])
        self.assertEqual(response_json["errors"], [])
        self.assertEqual(response_json["data"], {})

    """
    Verify that the register_person() view returns a valid 200 response when given a valid request.
    """
    @mock.patch('dateme_app.controller.register_person')
    @mock.patch('dateme_app.views.login')
    def test_register_person_view(self, mock_login, mock_register_person):

        # Arrange: mock dependencies
        status = Status(success=True, data={}, exceptions=[], errors=[], status_code=200)
        mock_login.return_value = status

        # mock a new person written to the database
        status = Status(success=True, data={"person":self.person_new}, exceptions=[], errors=[], status_code=200)
        mock_register_person.return_value = status

        # Act: call view
        url = reverse('dateme_app:register_person')        
        request_data = self.build_data(person=PersonSerializer(self.person_new).data)
        response = self.client.post(url, request_data, format='json')
        response_json = json.loads(response.content)

        # Assert: test response
        response_data = self.build_data(app=False, person=PersonSerializer(self.person_new).data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json["success"])
        self.assertEqual(response_json["exceptions"], [])
        self.assertEqual(response_json["errors"], [])
        self.assertEqual(response_json["data"], response_data)

    """
    Verify that the register_person() view returns a 500 response when an unexpected exception occurs.
    """
    @mock.patch('dateme_app.controller.register_person')
    @mock.patch('dateme_app.views.login')
    def test_register_person_view_exception(self, mock_login, mock_register_person):
        
        # Arrange: mock dependencies
        status = Status(success=True, data={}, exceptions=[], errors=[], status_code=200)
        mock_login.return_value = status

        # mock the view generating an exception
        exception_message = "Exception thrown by register_person()"
        mock_register_person.side_effect = Exception(exception_message)

        # Act: call view
        url = reverse('dateme_app:register_person')
        request_data = self.build_data(person=PersonSerializer(self.person_new).data)
        response = self.client.post(url, request_data, format='json')
        response_json = json.loads(response.content)

        # Assert: test response
        self.assertEqual(response.status_code, 500)
        self.assertFalse(response_json["success"])
        self.assertEqual(response_json["exceptions"], [exception_message])
        self.assertEqual(response_json["errors"], [])
        self.assertEqual(response_json["data"], {})

    """
    Verify that the register_person() view returns a 200 response and error 0201 when the user already exists.
    """
    @mock.patch('dateme_app.controller.register_person')
    @mock.patch('dateme_app.views.login')
    def test_register_person_view_multiple(self, mock_login, mock_register_person):
        
        # Arrange: mock dependencies
        status = Status(success=True, data={}, exceptions=[], errors=[], status_code=200)
        mock_login.return_value = status

        # mock trying to write an existing person as new to the database
        errors = ["020101"]
        status = Status(success=False, data={}, exceptions=[], errors=errors, status_code=200)
        mock_register_person.return_value = status

        # Act: call view
        url = reverse('dateme_app:register_person')
        request_data = self.build_data(person=PersonSerializer(self.person_a, exclude=['id']).data)
        response = self.client.post(url, request_data, format='json')
        response_json = json.loads(response.content)

        # Assert: test response
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response_json["success"])
        self.assertEqual(response_json["exceptions"], [])
        self.assertEqual(response_json["errors"], errors)
        self.assertEqual(response_json["data"], {})

    """
    Verify that the update_person() view returns a valid 200 response when given a valid request.
    """
    @mock.patch('dateme_app.controller.update_person')
    @mock.patch('dateme_app.views.login')
    def test_update_person_view(self, mock_login, mock_update_person):

        # Arrange: mock dependencies
        status = Status(success=True, data={}, exceptions=[], errors=[], status_code=200)
        mock_login.return_value = status

        # mock a change to an existing person
        person = self.person_a
        person.age_end = person.age_end + 1
        status = Status(success=True, data={"person":person}, exceptions=[], errors=[], status_code=200)
        mock_update_person.return_value = status

        # Act: call view
        url = reverse('dateme_app:update_person')        
        request_data = self.build_data(person=PersonSerializer(person).data)
        response = self.client.post(url, request_data, format='json')
        response_json = json.loads(response.content)

        # Assert: test response
        response_data = self.build_data(app=False, person=PersonSerializer(person).data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json["success"])
        self.assertEqual(response_json["exceptions"], [])
        self.assertEqual(response_json["errors"], [])
        self.assertEqual(response_json["data"], response_data)

    """
    Verify that the update_person() view returns a 500 response when an unexpected exception occurs.
    """
    @mock.patch('dateme_app.controller.update_person')
    @mock.patch('dateme_app.views.login')
    def test_update_person_view_exception(self, mock_login, mock_update_person):
        
        # Arrange: mock dependencies
        status = Status(success=True, data={}, exceptions=[], errors=[], status_code=200)
        mock_login.return_value = status

        # mock the view generating an exception
        exception_message = "Exception thrown by update_person()"
        mock_update_person.side_effect = Exception(exception_message)

        # Act: call view
        url = reverse('dateme_app:update_person')
        request_data = self.build_data(person=PersonSerializer(self.person_a).data)
        response = self.client.post(url, request_data, format='json')
        response_json = json.loads(response.content)

        # Assert: test response
        self.assertEqual(response.status_code, 500)
        self.assertFalse(response_json["success"])
        self.assertEqual(response_json["exceptions"], [exception_message])
        self.assertEqual(response_json["errors"], [])
        self.assertEqual(response_json["data"], {})

    """
    Verify that the update_person() view returns a 200 response and error 0201 when the user already exists.
    """
    @mock.patch('dateme_app.controller.update_person')
    @mock.patch('dateme_app.views.login')
    def test_update_person_view_multiple(self, mock_login, mock_update_person):
        
        # Arrange: mock dependencies
        status = Status(success=True, data={}, exceptions=[], errors=[], status_code=200)
        mock_login.return_value = status

        # mock trying to update a nonexistent person in the database
        errors = ["020201"]
        status = Status(success=False, data={}, exceptions=[], errors=errors, status_code=200)
        mock_update_person.return_value = status

        # Act: call view
        url = reverse('dateme_app:update_person')
        request_data = self.build_data(person=PersonSerializer(self.person_new).data)
        response = self.client.post(url, request_data, format='json')
        response_json = json.loads(response.content)

        # Assert: test response
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response_json["success"])
        self.assertEqual(response_json["exceptions"], [])
        self.assertEqual(response_json["errors"], errors)
        self.assertEqual(response_json["data"], {})

class ServiceAPITests(PearingTestCase):
    # TODO: Testing login will go here.    
    pass