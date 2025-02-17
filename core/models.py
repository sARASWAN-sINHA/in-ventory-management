'''Models for the project are defined here.'''


import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator

from .managers import UserManager
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that extends AbstractBaseUser and PermissionsMixin.
    Attributes:
        email (EmailField): The unique email address used as the identifier for the user.
        password (CharField): The password for the user.
        is_active (BooleanField): Indicates whether the user account is active. Defaults to True.
        is_staff (BooleanField): Indicates whether the user has staff status. Defaults to False.
        is_superuser (BooleanField): Indicates whether the user has superuser status. Defaults to False.
    Methods:
        None
    Meta:
        USERNAME_FIELD (str): The field used as the unique identifier for the user. Set to "email".
        REQUIRED_FIELDS (list): A list of fields that are required when creating a user. Set to ["password"].
    """
    email = models.EmailField(verbose_name="email_id", db_column="email", unique=True)
    password = models.CharField(db_column="password")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

class Profile(models.Model):

    """
    Profile model to store additional information about the user.

    Attributes:
        id (UUIDField): Id field for the Profile model.
        first_name (CharField): The first name of the user. Required.
        last_name (CharField): The last name of the user. Optional.
        designation (CharField): The designation of the user. Required.
        qualification (CharField): The qualification of the user.
        phone_number (CharField): The phone number of the user. Optional.
        address (TextField): The address of the user. Optional.
        user (OneToOneField): A one-to-one relationship with the User model. Acts as the primary key.
    """
    id= models.UUIDField(editable=False, primary_key=True, unique=True, default=uuid.uuid4)
    first_name= models.CharField(max_length=100, null=False, blank=False, validators=[MinLengthValidator(1)])
    last_name=models.CharField(max_length=100, blank=True, null=True)
    designation= models.CharField(max_length=100, null=False, blank=False)
    qualification=models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    user = models.OneToOneField(to="core.User", on_delete=models.CASCADE, related_name="profile")

    def save(self, *args, **kwargs):
        """
        Save the Profile instance after performing full validation.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The saved Profile instance.
        """
        self.full_clean()
        return super().save(*args, **kwargs)

class AssetType(models.Model):
    """
    AssetType model represents different types of assets in the inventory management system.
    Attributes:
        type (CharField): The main type of the asset. This field is required and must have at least 1 character.
        sub_type (CharField): The sub-type of the asset. This field is required and must have at least 1 character.
        group (CharField): The group to which the asset belongs. This field is required and must have at least 1 character.
        description (TextField): A detailed description of the asset. This field is optional.
    Properties:
        code (str): A property that generates a code by extracting parts of the type, sub_type, and group fields.
    """


    type = models.CharField(max_length=225, null=False, blank=False, validators=[MinLengthValidator(1)])
    sub_type = models.CharField(max_length=225, null=False, blank=False, validators=[MinLengthValidator(1)])
    group = models.CharField(max_length=225, null=False, blank=False, validators=[MinLengthValidator(1)])
    description = models.TextField(blank=True, null=True)

    @property
    def code(self) -> str:
        extract_code = lambda txt_with_code: txt_with_code.split("(")[-1][:-1]
        type_code = f'{extract_code(self.type)}-{extract_code(self.sub_type)}-{extract_code(self.group)}'
        return type_code


class Asset(models.Model):
    """
    Asset model represents individual assets in the inventory management system.
    Attributes:
        name (str): The name of the asset. It is a required field with a maximum length of 100 characters.
        description (str, optional): A brief description of the asset. This field is optional and can be left blank.
        quantity (int): The quantity of the asset available in the inventory. It is a required field and must be a non-negative integer.
        current_owner (User): The current owner of the asset. It is a required field and is linked to the User model.
        asset_type (AssetType): The type of asset. It is a required field and is linked to the AssetType model.
        location (str): The location where the asset is stored. It is a required field with a maximum length of 100 characters.
        manufacturer (str): The manufacturer of the asset. It is a required field with a maximum length of 100 characters.
    """

    name = models.CharField(max_length=100, null=False, blank=False, validators=[MinLengthValidator(5)])
    description = models.CharField(max_length=200, blank=True, null=True, validators=[MinLengthValidator(10)])
    quantity = models.PositiveIntegerField(null=False, blank=False)
    current_owner = models.ForeignKey(to="core.User", on_delete=models.CASCADE, related_name="assets")
    asset_type = models.ForeignKey(to="core.AssetType", on_delete=models.CASCADE, related_name="assets")
    location = models.CharField(max_length=100, null=False, blank=False, validators=[MinLengthValidator(1)])
    manufacturer = models.CharField(max_length=100, null=False, blank=False, validators=[MinLengthValidator(1)])



    def save(self, *args, **kwargs):
        """
        Save the Asset instance after performing full validation.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The saved Asset instance.
        """
        self.full_clean()
        return super().save(*args, **kwargs)