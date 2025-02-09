'''Models for the project are defined here.'''


import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinLengthValidator


class UserManager(BaseUserManager):
    """
    Custom user manager for handling user creation and superuser creation.

    Methods
    -------
    create_user(email, password, **extra_fields)
        Creates and returns a regular user with the given email and password.

    create_superuser(email, password, **extra_fields)
        Creates and returns a superuser with the given email and password.
    """

    def create_user(self, email, password, **extra_fields):

        """
        Creates and returns a regular user with the given email and password.

        Parameters
        ----------
        email : str
            The email address of the user.
        password : str
            The password for the user.
        **extra_fields : dict
            Additional fields for the user.

        Raises
        ------
        ValueError
            If the email or password is not provided.

        Returns
        -------
        user : User
            The created user instance.
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        if email is None or email == "":
            raise ValueError("Email is a mandatory field1")
        if password is None or password == "":
            raise ValueError("Password is a mandatory field1")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):

        """
        Creates and returns a superuser with the given email and password.

        Parameters
        ----------
        email : str
            The email address of the superuser.
        password : str
            The password for the superuser.
        **extra_fields : dict
            Additional fields for the superuser.

        Raises
        ------
        ValueError
            If is_staff, is_superuser, or is_active is not set to True.

        Returns
        -------
        superuser : User
            The created superuser instance.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") == False:
            raise ValueError("is_staff must be True for superuser!")
        if extra_fields.get("is_superuser") == False:
            raise ValueError("is_superuser must be True for superuser!")
        if extra_fields.get("is_active") == False:
            raise ValueError("is_active must be True for superuser!")

        superuser = self.create_user(email, password, **extra_fields)
        return superuser




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

