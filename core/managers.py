from django.contrib.auth.models import BaseUserManager

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

