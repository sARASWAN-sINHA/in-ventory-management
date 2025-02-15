"""Test cases for the profile API"""

from unittest import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from  django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from core.models import Profile



PROFILE_CREATE_URL = reverse('profile-list')
PROFILE_RETRIEVE_URL = lambda profile_id: reverse('profile-detail', args=[profile_id])
PROFILE_UPDATE_URL = lambda profile_id: reverse('profile-detail', args=[profile_id])

def create_profile(user):
    """Utility function to create a profile"""
    profile = Profile.objects.create(
            first_name='test',
            last_name='user',
            designation='developer',
            qualification='btech',
            phone_number= '123456',
            address= 'test address',
            user=user,
        )
    return profile

class PublicTestProfile(TestCase):
    """
    Test suite for public access to user profiles.
    This test case ensures that unauthorized users cannot retrieve or create user profiles.
    -------
    Methods

    setUp():
        Sets up the test client and creates a test user.
    test_retrieve_profile():
        Tests that retrieving a user profile without authorization returns a 401 status code.
    test_create_profile():
        Tests that creating a user profile without authorization returns a 401 status code.
    """


    def setUp(self):
        """Sets up the test client and creates a test user."""
        self.client = APIClient()
        get_user_model().objects.filter(email='testuser@example.com').delete()
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )

    def test_retrieve_profile(self):
        """ Tests that retrieving a user profile without authorization returns a 401 status code."""
        profile = create_profile(self.user)
        res = self.client.get(PROFILE_RETRIEVE_URL(profile_id=profile.id))
        self.assertEqual(res.status_code, 401)

    def test_create_profile(self):
        """Tests that creating a user profile without authorization returns a 401 status code."""
        payload = {
                'first_name': 'test1',
                'last_name': 'user1',
                'designation': 'developer1',
                'qualification': 'btech1',
                'phone_number': '1234567',
                'address': 'test address1',
        }
        res = self.client.post(PROFILE_CREATE_URL, payload)
        self.assertEqual(res.status_code, 401)


class PrivateTestProfile(TestCase):
    """
    Test suite for the user profile management API.
    This class contains tests for creating, retrieving, updating, and validating user profiles.
    It uses Django's TestCase and APIClient for testing the API endpoints.
    -------
    Methods

    setUp():
        Sets up the test client and creates a test user.
    test_create_profile():
        Tests the creation of a user profile with valid data.
    test_retrieve_profile():
        Tests retrieving a user profile by its ID.
    test_update_profile():
        Tests updating a user profile with new data.
    test_create_profile_without_firstname():
        Tests creating a user profile without a first name, expecting a 400 status code.
    test_create_profile_without_designation():
        Tests creating a user profile without a designation, expecting a 400 status code.
    """

    def setUp(self):
        """Sets up the test client and creates a test user."""
        self.client = APIClient()

        get_user_model().objects.filter(email='testuser@example.com').delete()

        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(self.user)

    def test_create_profile(self):
        """Tests the creation of a user profile with valid data."""
        payload = {
            'first_name': 'test',
            'last_name': 'user',
            'designation': 'developer',
            'qualification': 'btech',
            'phone_number': '123456',
            'address': 'test address',
            # 'user': self.user
        }
        res = self.client.post(PROFILE_CREATE_URL, payload)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        self.assertTrue(Profile.objects.filter(first_name='test').exists())
        self.assertTrue(Profile.objects.filter(phone_number='123456').exists())

    def test_retrieve_profile(self):
        """Tests retrieving a user profile by its ID."""
        profile = create_profile(self.user)
        res = self.client.get(PROFILE_RETRIEVE_URL(profile.id))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['first_name'], profile.first_name)
        self.assertEqual(res.data['phone_number'], profile.phone_number)

    def test_update_profile(self):
        """Tests updating a user profile with new data."""
        profile = create_profile(self.user)
        payload = {
            'first_name': 'test1',
            'last_name': 'user1',
            'designation': 'developer1',
            'qualification': 'btech1',
            'phone_number': '1234567',
            'address': 'test address1',
        }
        res = self.client.patch(PROFILE_UPDATE_URL(profile.id), payload)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['first_name'], payload['first_name'])
        self.assertEqual(res.data['phone_number'], payload['phone_number'])
        self.assertEqual(res.data['qualification'], payload['qualification'])
        self.assertEqual(res.data['designation'], payload['designation'])

    def test_create_profile_without_firstname(self):
        """Tests creating a user profile without a first name, expecting a 400 status code."""
        payload = {
            'first_name': '',
            'last_name': 'user',
            'designation': 'developer',
            'qualification': 'btech',
            'phone_number': '123456',
            'address': 'test address',
        }

        res = self.client.post(PROFILE_CREATE_URL, payload)
        self.assertEqual(res.status_code, 400)

    def test_create_profile_without_designation(self):
        """Tests creating a user profile without a first name, expecting a 400 status code."""
        payload = {
            'first_name': 'test',
            'last_name': 'user',
            'designation': '',
            'qualification': 'btech',
            'phone_number': '123456',
            'address': 'test address',
        }
        res = self.client.post(PROFILE_CREATE_URL, payload)

        self.assertEqual(res.status_code, 400)


