from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinLengthValidator


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

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
    email = models.EmailField(verbose_name="email_id", db_column="email", unique=True)
    password = models.CharField(db_column="password")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

class Profile(models.Model):
    first_name= models.CharField(max_length=100, null=False, blank=False, validators=[MinLengthValidator(1)])
    last_name=models.CharField(max_length=100, blank=True, null=True)
    designation= models.CharField(max_length=100, null=False, blank=False)
    qualification=models.CharField(max_length=100)

    user = models.OneToOneField(to="core.User", on_delete=models.CASCADE, related_name="profile", primary_key=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

