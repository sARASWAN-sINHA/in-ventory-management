"""Unit tests for models"""

from django.test import TestCase
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model

from ..models import Profile


def create_user(email, password):
    return get_user_model().objects.create_user(email=email, password=password)


def create_profile(user=None):
    first_name = "Test"
    last_name = "User"
    designation = "Test designation"
    qualification = "Test qualification"

    return Profile.objects.create(
        first_name=first_name,
        last_name=last_name,
        designation=designation,
        qualification=qualification,
        user=user,
    )


class TestUserModel(TestCase):
    """
    TestUserModel contains unit tests for user and superuser creation, ensuring that users are created with valid credentials and profiles, and
    that superusers have the correct permissions and attributes.

    It also includes tests to verify that users and superusers are not created with invalid or missing fields.
    """

    def test_user_creation(self):
        """Test to check if user is created successfully"""

        email = "test@user.com"
        password = "test_password"

        user = create_user(email, password)
        profile = create_profile(user=user)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

        self.assertEqual(user.profile, profile)

    def test_superuser_creation(self):
        """Test to check if superuser is created successfully"""
        email = "test@user.com"
        password = "test_password"

        superuser = get_user_model().objects.create_superuser(email, password)
        profile = create_profile(superuser)

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)

        self.assertEqual(superuser.profile, profile)

    def test_create_user_without_email(self):
        """Test to check if user is not created without email"""
        email = ""
        password = "test_password"

        with self.assertRaises(ValueError):
            create_user(email=email, password=password)

    def test_create_user_without_password(self):
        """Test to check if user is not created without password"""
        email = "test@user.com"
        password = ""

        with self.assertRaises(ValueError):
            create_user(email=email, password=password)

    def test_create_superuser_with_incorrect_extra_fields(self):
        """Test to check if superuser is not created with incorrect extra fields"""
        email = "test@user.com"
        password = "test_password"

        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email=email, password=password, is_superuser=False
            )
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email=email, password=password, is_staff=False
            )
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email=email, password=password, is_active=False
            )


class ProfileTestClass(TestCase):
    """
    Test suite for the Profile model.
    This class contains unit tests to verify the creation and validation of Profile instances.
    It includes tests to ensure that profiles are created successfully with valid data,
    and that appropriate validation errors are raised when required fields are missing.
    Attributes:
        first_name (str): The first name to be used for creating test profiles.
        last_name (str): The last name to be used for creating test profiles.
        designation (str): The designation to be used for creating test profiles.
        qualification (str): The qualification to be used for creating test profiles.
    Methods:
        create_user(email, password):
            Creates and returns a user with the given email and password.
        test_create_profile():
            Tests if a profile is created successfully with valid data.
        test_profile_without_first_name_or_designation():
            Tests if a profile is not created when the first name or designation is missing.
        test_profile_without_user():
            Tests if a profile is not created when the user is missing.
    """

    first_name = "Test"
    last_name = "User"
    designation = "Test designation"
    qualification = "Test qualification"

    def create_user(self, email, password):
        return get_user_model().objects.create_user(email=email, password=password)

    def test_create_profile(self):
        """Test to check if profile is created successfully"""
        user = self.create_user("test@user.com", "test123")

        profile = Profile.objects.create(
            first_name=ProfileTestClass.first_name,
            last_name=ProfileTestClass.last_name,
            designation=ProfileTestClass.designation,
            qualification=ProfileTestClass.qualification,
            user=user,
        )
        self.assertEqual(user, profile.user)
        self.assertEqual(profile.first_name, ProfileTestClass.first_name)
        self.assertEqual(profile.last_name, ProfileTestClass.last_name)
        self.assertEqual(profile.designation, ProfileTestClass.designation)
        self.assertEqual(profile.qualification, ProfileTestClass.qualification)

    def test_profile_without_first_name_or_designation(self):
        """Test to check if profile is not created without first name or designation"""

        user = self.create_user("test@user.com", "test123")

        with self.assertRaises(ValidationError):
            Profile.objects.create(
                first_name="",
                last_name=ProfileTestClass.last_name,
                designation=ProfileTestClass.designation,
                qualification=ProfileTestClass.qualification,
                user=user,
            )
        with self.assertRaises(ValidationError):
            Profile.objects.create(
                first_name=ProfileTestClass.first_name,
                last_name=ProfileTestClass.last_name,
                designation="",
                qualification=ProfileTestClass.qualification,
                user=user,
            )

    def test_profile_without_user(self):
        """Test to check if profile is not created without user"""
        with self.assertRaises(ValidationError):
            Profile.objects.create(
                first_name=ProfileTestClass.first_name,
                last_name=ProfileTestClass.last_name,
                designation=ProfileTestClass.designation,
                qualification=ProfileTestClass.qualification,
            )
