from email.headerregistry import Group
from django.urls import reverse
from django.contrib.auth import get_user_model

from unittest import TestCase
from rest_framework.test import APIClient

from core.models import Asset, AssetType

ASSET_CREATE_URL = reverse("asset-list")
ASSET_LIST_URL = reverse("asset-list")

ASSET_DELETE_URL = lambda asset_id: reverse("asset-detail", agrs=[asset_id])
ASSET_RETRIEVE_URL = lambda asset_id: reverse("asset-detail", agrs=[asset_id])


def create_asset(
    user,
    asset_type,
    name="Test Asset",
    description="This is a test asset.",
    manufacturer="Test Manufacturer",
    location="Test Location",
    quantity=1,
):
    asset = Asset.objects.create(
        name=name,
        description=description,
        manufacturer=manufacturer,
        location=location,
        quantity=quantity,
        user=user,
        asset_type=asset_type,
    )
    return asset


def create_asset_group(
    type="Test Type(HDW)", sub_type="Test Sub Type(EOD)", group="Test Group(HDN)"
):
    return AssetType.objects.get_or_create(
        type=type,
        sub_type=sub_type,
        group=group,
    )


class PrivateTestAssetForNormalUsers(TestCase):
    """Tests for the asset endpoints for normal users."""

    def setUp(self):
        """Sets up the test client and creates a test user."""
        self.client = APIClient()
        if get_user_model().objects.filter(email="test@example.com").exists():
            self.user = get_user_model().objects.get(email="test@example.com")

        else:
            self.user = get_user_model().objects.create_user(
                email="test@example.com",
                password="testpassword",
            )

        normal_user_group = Group.object.create(name="Normal user")
        self.user.groups.add(normal_user_group)


        self.asset_1 = create_asset(self.user, create_asset_group())
        self.asset_2 = create_asset(self.user, create_asset_group(group="Test Group 2(BOX)"))

        if get_user_model().objects.filter(email="test2@example.com").exists():
            self.another_user = get_user_model().objects.get(email="test2@example.com")
        else:
            self.another_user = get_user_model().objects.create_user(
                email="test2@example.com",
                password="testpassword",
            )
        normal_user_group = Group.object.create(name="Normal user")
        self.another_user.groups.add(normal_user_group)


        self.asset_3 = create_asset(self.another_user, create_asset_group(group="Test Group 3(PRNTR)"))
        self.asset_4 = create_asset(self.another_user, create_asset_group(group="Test Group 4(KEYB)"))

        self.client.force_authenticate(user=self.user)

    def test_create_asset(self):
        """Tests that authorized normal users cannot create assets."""
        payload = {
            "name": "Test Asset",
            "description": "This is a test asset.",
            "location": "Test Location",
            "manufacturer": "Test Manufacturer",
            "quantity": 1,
            "asset_type": "HDW-EOD-HDN",
        }

        res = self.client.post(ASSET_CREATE_URL, payload)
        self.assertEqual(res.status_code, 403)

    def test_list_asset(self):
        """Tests that authorized normal users can retrieve all assets that only belong to them."""
        res = self.client.get(ASSET_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.count, 2)
        self.assertEqual(res.data[0]["asset_type"], "HDW-EOD-HDN")
        self.assertEqual(res.data[1]["asset_type"], "HDW-EOD-BOX")

        self.client.logout()

        self.client.force_authenticate(user=self.another_user)

        res = self.client.get(ASSET_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.count, 2)
        self.assertEqual(res.data[0]["asset_type"], "HDW-EOD-PRNTR")
        self.assertEqual(res.data[1]["asset_type"], "HDW-EOD-KEYB")

    def test_retrieve_asset(self):
        """Tests that authorized normal users can retrieve a specific asset assigned to him/her."""
        res = self.client.get(ASSET_RETRIEVE_URL(self.asset_1.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["name"], self.asset_1.name)

        res = self.client.get(ASSET_RETRIEVE_URL(self.asset_3.id))
        self.assertEqual(res.status_code, 403)


    def test_update_asset(self):
        """Tests that authorized normal users cannot update an asset."""
        payload = {
            "name": "Test Asset",
            "description": "This is a test asset.",
            "location": "Test Location",
            "manufacturer": "Test Manufacturer",
            "quantity": 1,
            "asset_type": "HDW-EOD-HDN",
        }

        res = self.client.put(ASSET_RETRIEVE_URL(self.asset_1.id), payload)
        self.assertEqual(res.status_code, 403)

        res = self.client.put(ASSET_RETRIEVE_URL(self.asset_2.id), payload)
        self.assertEqual(res.status_code, 403)

    def test_delete_asset(self):
        """Tests that authorized users cannot delete an asset."""
        res = self.client.delete(ASSET_DELETE_URL(self.asset_1.id))
        self.assertEqual(res.status_code, 403)

        res = self.client.delete(ASSET_DELETE_URL(self.asset_2.id))
        self.assertEqual(res.status_code, 403)

class PrivateTestAssetForAssetModerators(TestCase):
    """Tests for the asset endpoints for asset moderators."""

    def setUp(self):
        """Sets up the test client and creates a test user."""
        self.client = APIClient()
        if get_user_model().objects.filter(email="test@example.com").exists():
            self.user = get_user_model().objects.get(email="test@example.com")

        else:
            self.user = get_user_model().objects.create_user(
                email="test@example.com",
                password="testpassword",
            )

        asset_moderator_group = Group.object.create(name="Asset moderator")
        self.user.groups.add(asset_moderator_group)


        self.asset_1 = create_asset(self.user, create_asset_group())
        self.asset_2 = create_asset(self.user, create_asset_group(group="Test Group 2(BOX)"))

        if get_user_model().objects.filter(email="test2@example.com").exists():
            self.another_user = get_user_model().objects.get(email="test2@example.com")
        else:
            self.another_user = get_user_model().objects.create_user(
                email="test2@example.com",
                password="testpassword",
            )
        asset_moderator_group = Group.object.create(name="Asset moderator")
        self.another_user.groups.add(asset_moderator_group)


        self.asset_3 = create_asset(self.another_user, create_asset_group(group="Test Group 3(PRNTR)"))
        self.asset_4 = create_asset(self.another_user, create_asset_group(group="Test Group 4(KEYB)"))

        self.client.force_authenticate(user=self.user)

    def test_create_asset(self):
        """Tests that authorized asset moderators can create assets."""
        payload = {
            "name": "Test Asset",
            "description": "This is a test asset.",
            "location": "Test Location",
            "manufacturer": "Test Manufacturer",
            "quantity": 1,
            "asset_type": "HDW-EOD-HDN",
        }

        res = self.client.post(ASSET_CREATE_URL, payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["name"], "Test Asset")
        self.assertEqual(res.data["asset_type"], "HDW-EOD-HDN")

    def test_list_asset(self):
        """Tests that authorized asset moderators can retrieve all assets."""
        res = self.client.get(ASSET_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.count, 4)
        self.assertEqual(res.data[0]["asset_type"], "HDW-EOD-HDN")
        self.assertEqual(res.data[1]["asset_type"], "HDW-EOD-BOX")
        self.assertEqual(res.data[2]["asset_type"], "HDW-EOD-PRNTR")
        self.assertEqual(res.data[3]["asset_type"], "HDW-EOD-KEYB")

    def test_retrieve_asset(self):
        """Tests that authorized asset moderators can retrieve a specific asset."""
        res = self.client.get(ASSET_RETRIEVE_URL(self.asset_1.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["name"], self.asset_1.name)

        res = self.client.get(ASSET_RETRIEVE_URL, {"id": self.asset_2.id})
        self.assertEqual(res.status_code, 200)

    def test_update_asset(self):
        """Tests that authorized asset moderators cannot update an asset."""
        payload = {
            "name": "Test Asset",
            "description": "This is a test asset.",
            "location": "Test Location",
            "manufacturer": "Test Manufacturer",
            "quantity": 200,
            "asset_type": "HDW-EOD-HDN",
        }

        res = self.client.put(ASSET_RETRIEVE_URL(self.asset_1.id), payload)
        self.assertEqual(res.status_code, 403)

    def test_delete_asset(self):
        """Tests that authorized asset moderators cannot delete an asset """
        res = self.client.delete(ASSET_DELETE_URL(self.asset_1.id))
        self.assertEqual(res.status_code, 403)

    def create_asset_with_quantity_zero(self):
        """Tests that authorized asset moderators cannot create an asset with quantity zero."""
        payload = {
            "name": "Test Asset",
            "description": "This is a test asset.",
            "location": "Test Location",
            "manufacturer": "Test Manufacturer",
            "quantity": 0,
            "asset_type": "HDW-EOD-HDN",
        }

        res = self.client.post(ASSET_CREATE_URL, payload)
        self.assertEqual(res.status_code, 403)

class PrivateTestAssetForAssetAdmin(TestCase):
    """Tests for the asset endpoints for asset admins."""

    def setUp(self):
        """Sets up the test client and creates a test user."""
        self.client = APIClient()
        if get_user_model().objects.filter(email="test@example.com").exists():
            self.user = get_user_model().objects.get(email="test@example.com")

        else:
            self.user = get_user_model().objects.create_user(
                email="test@example.com",
                password="testpassword",
            )

        asset_admin_group = Group.object.create(name="Asset Admin")
        self.user.groups.add(asset_admin_group)


        self.asset_1 = create_asset(self.user, create_asset_group())
        self.asset_2 = create_asset(self.user, create_asset_group(group="Test Group 2(BOX)"))

        if get_user_model().objects.filter(email="test2@example.com").exists():
            self.another_user = get_user_model().objects.get(email="test2@example.com")
        else:
            self.another_user = get_user_model().objects.create_user(
                email="test2@example.com",
                password="testpassword",
            )
        asset_admin_group = Group.object.create(name="Normal user")
        self.another_user.groups.add(asset_admin_group)


        self.asset_3 = create_asset(self.another_user, create_asset_group(group="Test Group 3(PRNTR)"))
        self.asset_4 = create_asset(self.another_user, create_asset_group(group="Test Group 4(KEYB)"))

        self.client.force_authenticate(user=self.user)

    def test_create_asset(self):
        """Tests that authorized asset moderators can create assets."""
        payload = {
            "name": "Test Asset",
            "description": "This is a test asset.",
            "location": "Test Location",
            "manufacturer": "Test Manufacturer",
            "quantity": 1,
            "asset_type": "HDW-EOD-HDN",
        }

        res = self.client.post(ASSET_CREATE_URL, payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["name"], "Test Asset")
        self.assertEqual(res.data["asset_type"], "HDW-EOD-HDN")

    def test_list_asset(self):
        """Tests that authorized asset moderators can retrieve all assets."""
        res = self.client.get(ASSET_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.count, 4)
        self.assertEqual(res.data[0]["asset_type"], "HDW-EOD-HDN")
        self.assertEqual(res.data[1]["asset_type"], "HDW-EOD-BOX")
        self.assertEqual(res.data[2]["asset_type"], "HDW-EOD-PRNTR")
        self.assertEqual(res.data[3]["asset_type"], "HDW-EOD-KEYB")

    def test_retrieve_asset(self):
        """Tests that authorized asset moderators can retrieve a specific asset."""
        res = self.client.get(ASSET_RETRIEVE_URL(self.asset_1.id))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["name"], self.asset_1.name)

        res = self.client.get(ASSET_RETRIEVE_URL, {"id": self.asset_2.id})
        self.assertEqual(res.status_code, 200)

    def test_update_asset(self):
        """Tests that authorized asset moderators cannot update an asset."""
        payload = {
            "name": "Test Asset",
            "description": "This is a test asset.",
            "location": "Test Location",
            "manufacturer": "Test Manufacturer",
            "quantity": 200,
            "asset_type": "HDW-EOD-HDN",
        }

        res = self.client.put(ASSET_RETRIEVE_URL(self.asset_1.id), payload)
        self.assertEqual(res.status_code, 200)

    def test_delete_asset(self):
        """Tests that authorized asset moderators cannot delete an asset """
        res = self.client.delete(ASSET_DELETE_URL(self.asset_1.id))
        self.assertEqual(res.status_code, 403)

    def create_asset_with_quantity_zero(self):
        """Tests that authorized asset moderators cannot create an asset with quantity zero."""
        payload = {
            "name": "Test Asset",
            "description": "This is a test asset.",
            "location": "Test Location",
            "manufacturer": "Test Manufacturer",
            "quantity": 0,
            "asset_type": "HDW-EOD-HDN",
        }

        res = self.client.post(ASSET_CREATE_URL, payload)
        self.assertEqual(res.status_code, 200)