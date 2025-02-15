"""Unit test for asset models"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError



from ..models import Asset, AssetType
from .test_user_models import create_user

def create_asset(name, description, quantity, user, asset_type, location, manufacturer):
    """
    Create and return a new Asset instance.
    Args:
        name (str): The name of the asset.
        description (str): A brief description of the asset.
        quantity (int): The quantity of the asset.
        user (User): The current owner of the asset.
        asset_type (AssetType): The type/category of the asset.
        location (Location): The location where the asset is stored.
        manufacturer (Manufacturer): The manufacturer of the asset.
    Returns:
        Asset: The created Asset instance.
    """

    return Asset.objects.create(
        name=name,
        description=description,
        quantity=quantity,
        current_owner=user,
        asset_type=asset_type,
        location=location,
        manufacturer=manufacturer,
    )

class TestAssetTypeModel(TestCase):
    """
    Test case for the AssetType model.
    This test case includes methods to create and validate AssetType instances.
    Attributes:
        type (str): The type of the asset.
        sub_type (str): The sub-type of the asset.
        group (str): The group of the asset.
        description (str): The description of the asset.
        code (str): The code of the asset.
    Methods:
        create_asset_type(asset_type, asset_description, sub_type, group):
            Creates and returns an AssetType instance with the given attributes.
        test_create_asset_type():
            Tests the creation of an AssetType instance and validates its attributes.
    """



    type="Test Asset Type(HDW)"
    sub_type="Test Asset Sub Type(CABLE)"
    group="Test Asset Group(ETH)"
    description="Test Asset Type Description"
    code="HDW-CABLE-ETH"

    def create_asset_type(self, asset_type="Test Asset Type(HDW)", asset_description="Test Asset Type Description", sub_type="Test Asset Sub Type(CABLE)", group="Test Asset Group(ETH)"):
        """
        Creates and returns an AssetType instance with the given parameters.
        Args:
            asset_type (str): The type of the asset. Default is "Test Asset Type(HDW)".
            asset_description (str): The description of the asset type. Default is "Test Asset Type Description".
            sub_type (str): The sub-type of the asset. Default is "Test Asset Sub Type(CABLE)".
            group (str): The group of the asset. Default is "Test Asset Group(ETH)".
        Returns:
            AssetType: The created AssetType instance.
        """


        return AssetType.objects.create(
            type=asset_type,
            description=asset_description,
            sub_type=sub_type,
            group=group,

        )


    def test_create_asset_type(self):
        """
        Test the creation of an asset type.
        This test verifies that an asset type can be created with the specified
        attributes and that the created asset type matches the expected values.
        Steps:
        1. Create an asset type using the `create_asset_type` method with the
           attributes from `TestAssetTypeModel`.
        2. Assert that the created asset type's attributes match the expected
           values from `TestAssetTypeModel`.
        Asserts:
        - The type of the created asset type matches `TestAssetTypeModel.type`.
        - The description of the created asset type matches `TestAssetTypeModel.description`.
        - The sub_type of the created asset type matches `TestAssetTypeModel.sub_type`.
        - The group of the created asset type matches `TestAssetTypeModel.group`.
        - The code of the created asset type matches `TestAssetTypeModel.code`.
        """


        test_asset_type = self.create_asset_type(
            TestAssetTypeModel.type,
            TestAssetTypeModel.description,
            TestAssetTypeModel.sub_type,
            TestAssetTypeModel.group,
        )

        self.assertEqual(test_asset_type.type, TestAssetTypeModel.type)
        self.assertEqual(test_asset_type.description, TestAssetTypeModel.description)
        self.assertEqual(test_asset_type.sub_type, TestAssetTypeModel.sub_type)
        self.assertEqual(test_asset_type.group, TestAssetTypeModel.group)
        self.assertEqual(test_asset_type.code, TestAssetTypeModel.code)

class TestAssetModel(TestCase):
    """
        Test suite for the Asset model.
        This test suite contains various test cases to validate the functionality and constraints
        of the Asset model in the asset inventory management system. The tests cover scenarios
        such as creating assets with valid and invalid attributes, ensuring proper validation
        for fields like quantity, name, description, location, and manufacturer.
        Test Cases:
        - `test_create_asset`: Verifies the creation of an asset with valid attributes.
        - `test_create_asset_with_negative_quantity`: Ensures that creating an asset with a negative quantity raises a ValidationError.
        - `test_create_asset_with_name_less_than_five_characters`: Ensures that creating an asset with a name shorter than five characters raises a ValidationError.
        - `test_create_asset_with_no_type_code`: Ensures that creating an asset without specifying an asset type code raises a ValidationError.
        - `test_create_asset_with_no_location`: Ensures that creating an asset without specifying a location raises a ValidationError.
        - `create_asset_with_no_manufacturer`: Ensures that creating an asset without specifying a manufacturer raises a ValidationError.
        - `test_create_asset_with_description_less_than_five_characters`: Ensures that creating an asset with a description shorter than five characters raises a ValidationError.
        Helper Methods:
        - `create_asset_type`: Creates and returns an AssetType instance with the given parameters.
        - `create_new_user`: Creates a new user with the specified email and password.
        Attributes:
        - `name`: The name of the asset.
        - `description`: The description of the asset.
        - `quantity`: The quantity of the asset.
        - `location`: The location of the asset.
        - `manufacturer`: The manufacturer of the asset.
    """



    name="Test Asset"
    description="Test Asset Description"
    quantity=1
    location="Test Location"
    manufacturer="Test Manufacturer"


    def create_asset_type(self, asset_type="Test Asset Type(HDW)", asset_description="Test Asset Type Description", sub_type="Test Asset Sub Type(CABLE)", group="Test Asset Group(ETH)"):
        """
            Creates and returns an AssetType instance with the given parameters.
            Args:
                asset_type (str): The type of the asset. Default is "Test Asset Type(HDW)".
                asset_description (str): The description of the asset type. Default is "Test Asset Type Description".
                sub_type (str): The sub-type of the asset. Default is "Test Asset Sub Type(CABLE)".
                group (str): The group of the asset. Default is "Test Asset Group(ETH)".
            Returns:
                AssetType: The created AssetType instance.
        """

        # if AssetType.objects.filter(code=asset_code).exists():
        #     return AssetType.objects.get(code=asset_code)

        return AssetType.objects.create(
            type=asset_type,
            description=asset_description,
            sub_type=sub_type,
            group=group,

        )



    def create_new_user(self):
        """
            Creates a new user with the specified email and password.
            This method first deletes any existing user with the email "user@example.com"
            to ensure that the new user can be created without conflicts. It then creates
            and returns a new user with the email "user@example.com" and password "password12345".
            Returns:
                User: The newly created user object.
        """
        get_user_model().objects.filter(email="user@example.com").delete()
        test_user = create_user("user@example.com", "password12345")
        return test_user

    def test_create_asset(self):
        """
            Test the creation of an asset.
            This test verifies that an asset can be created with the specified attributes
            and that the created asset's attributes match the expected values.
            Steps:
            1. Create a new user.
            2. Create a new asset type.
            3. Create a new asset with the specified attributes.
            4. Assert that the created asset's attributes match the expected values.
            Asserts:
            - The asset's name matches the expected name.
            - The asset's description matches the expected description.
            - The asset's quantity matches the expected quantity.
            - The asset's current owner's email matches the expected user's email.
            - The asset's type matches the expected asset type.
            - The asset's location matches the expected location.
            - The asset's manufacturer matches the expected manufacturer.
        """
        test_user = self.create_new_user()
        test_asset_type = self.create_asset_type()

        test_asset = create_asset(
            name=TestAssetModel.name,
            description=TestAssetModel.description,
            quantity=TestAssetModel.quantity,
            user=test_user,
            asset_type=test_asset_type,
            location=TestAssetModel.location,
            manufacturer=TestAssetModel.manufacturer
        )

        self.assertEqual(test_asset.name, TestAssetModel.name)
        self.assertEqual(test_asset.description, TestAssetModel.description)
        self.assertEqual(test_asset.quantity, TestAssetModel.quantity)
        self.assertEqual(test_asset.current_owner.email, test_user.email)
        self.assertEqual(test_asset.asset_type, test_asset_type)
        self.assertEqual(test_asset.location, TestAssetModel.location)
        self.assertEqual(test_asset.manufacturer, TestAssetModel.manufacturer)

    def test_create_asset_with_negative_quantity(self):
        """
            Test that creating an asset with a negative quantity raises a ValidationError.
            This test ensures that the `create_asset` function does not allow the creation
            of an asset with a negative quantity. It verifies that a ValidationError is
            raised when attempting to create such an asset.
            The test uses the following parameters:
            - name: The name of the asset, taken from TestAssetModel.name.
            - description: The description of the asset, taken from TestAssetModel.description.
            - quantity: Set to -1 to test the negative quantity validation.
            - user: A new user created by the create_new_user method.
            - asset_type: An asset type created by the create_asset_type method.
            - location: The location of the asset, taken from TestAssetModel.location.
            - manufacturer: The manufacturer of the asset, taken from TestAssetModel.manufacturer.
            The test expects a ValidationError to be raised when the asset is created with
            a negative quantity.
        """
        with self.assertRaises(ValidationError):
            create_asset(
                name=TestAssetModel.name,
                description=TestAssetModel.description,
                quantity=-1,
                user=self.create_new_user(),
                asset_type=self.create_asset_type(),
                location=TestAssetModel.location,
                manufacturer=TestAssetModel.manufacturer
            )
    def test_create_asset_with_name_less_than_five_characters(self):
        """
            Test that creating an asset with a name less than five characters raises a ValidationError.
            This test ensures that the asset creation process enforces a minimum length constraint
            on the asset name. If the name provided is less than five characters, a ValidationError
            should be raised.
            Steps:
            1. Attempt to create an asset with a name "Some" (which is less than five characters).
            2. Verify that a ValidationError is raised.
            Expected Result:
            A ValidationError is raised due to the asset name being too short.
        """
        with self.assertRaises(ValidationError):
            create_asset(
                name="Some",
                description=TestAssetModel.description,
                quantity=TestAssetModel.quantity,
                user=self.create_new_user(),
                asset_type=self.create_asset_type(),
                location=TestAssetModel.location,
                manufacturer=TestAssetModel.manufacturer
            )

    def test_create_asset_with_no_type_code(self):
        """
            Test case for creating an asset without specifying an asset type code.
            This test ensures that attempting to create an asset without providing
            an asset type code raises a ValidationError.
            The following attributes are used for the asset creation:
            - name: The name of the asset.
            - description: A brief description of the asset.
            - quantity: The quantity of the asset.
            - user: The user associated with the asset.
            - asset_type: Set to None to simulate missing asset type code.
            - location: The location of the asset.
            - manufacturer: The manufacturer of the asset.
            The test expects a ValidationError to be raised when the asset type code
            is not provided.
        """

        with self.assertRaises(ValidationError):
            create_asset(
                name=TestAssetModel.name,
                description=TestAssetModel.description,
                quantity=TestAssetModel.quantity,
                user=self.create_new_user(),
                asset_type=None,
                location=TestAssetModel.location,
                manufacturer=TestAssetModel.manufacturer
            )

    def test_create_asset_with_no_location(self):
        """
            Test case for creating an asset without specifying a location.
            This test ensures that a ValidationError is raised when attempting to create an asset
            with an empty or None location. The test uses the `create_asset` function with the
            following parameters:
            - name: The name of the asset.
            - description: The description of the asset.
            - quantity: The quantity of the asset.
            - user: A user object created by `self.create_new_user()`.
            - asset_type: An asset type object created by `self.create_asset_type()`.
            - location: An empty string or None, which should trigger the ValidationError.
            - manufacturer: The manufacturer of the asset.
            The test performs two assertions:
            1. Asserts that a ValidationError is raised when the location is an empty string.
            2. Asserts that a ValidationError is raised when the location is None.
        """

        with self.assertRaises(ValidationError):
            create_asset(
                name=TestAssetModel.name,
                description=TestAssetModel.description,
                quantity=TestAssetModel.quantity,
                user=self.create_new_user(),
                asset_type=self.create_asset_type(),
                location="",
                manufacturer=TestAssetModel.manufacturer
            )
        with self.assertRaises(ValidationError):
            create_asset(
                name=TestAssetModel.name,
                description=TestAssetModel.description,
                quantity=TestAssetModel.quantity,
                user=self.create_new_user(),
                asset_type=self.create_asset_type(),
                location=None,
                manufacturer=TestAssetModel.manufacturer
            )

    def create_asset_with_no_manufacturer(self):
        """
            Test the creation of an asset without a manufacturer.
            This test ensures that attempting to create an asset without specifying
            a manufacturer (either as an empty string or None) raises a ValidationError.
            The test performs the following checks:
            1. Attempts to create an asset with an empty string as the manufacturer and expects a ValidationError.
            2. Attempts to create an asset with None as the manufacturer and expects a ValidationError.
            Raises:
                ValidationError: If the asset is created without a manufacturer.
        """

        with self.assertRaises(ValidationError):
            create_asset(
                name=TestAssetModel.name,
                description=TestAssetModel.description,
                quantity=TestAssetModel.quantity,
                user=self.create_new_user(),
                asset_type=self.create_asset_type(),
                location=TestAssetModel.location,
                manufacturer=""
            )
        with self.assertRaises(ValidationError):
            create_asset(
                name=TestAssetModel.name,
                description=TestAssetModel.description,
                quantity=TestAssetModel.quantity,
                user=self.create_new_user(),
                asset_type=self.create_asset_type(),
                location=TestAssetModel.location,
                manufacturer=None
            )
    def test_create_asset_with_description_less_than_five_characters(self):
        """
            Test that creating an asset with a description less than five characters
            raises a ValidationError.
            This test ensures that the asset creation process enforces a minimum
            length requirement for the description field. An asset with a description
            shorter than five characters should not be allowed and should raise a
            ValidationError.
            Steps:
            1. Attempt to create an asset with a description of "Some" (4 characters).
            2. Verify that a ValidationError is raised.
            Expected Result:
            A ValidationError is raised, indicating that the description is too short.
        """

        with self.assertRaises(ValidationError):
            create_asset(
                name=TestAssetModel.name,
                description="Some",
                quantity=TestAssetModel.quantity,
                user=self.create_new_user(),
                asset_type=self.create_asset_type(),
                location=TestAssetModel.location,
                manufacturer=TestAssetModel.manufacturer
            )





