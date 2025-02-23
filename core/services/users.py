from typing import List
from django.contrib.auth import get_user_model, models
from ..models import User

from django.db.models.query import QuerySet


class UserService:
    @staticmethod
    def get_user_by_email(email: str) -> User | str:
        try:
            return get_user_model().objects.get(email=email)
        except User.DoesNotExist :
            return "User not found"

    @staticmethod
    def get_user_by_id(id: int) -> User | str:
        try:
            return get_user_model().objects.get(id=id)
        except User.DoesNotExist:
            return "User not found"

    @staticmethod
    def get_user_groups(user: User) -> List[models.Group]:
        return user.groups.all()


    @staticmethod
    def is_user_in_group(user: User, group_name: str) -> bool:
        return user.groups.filter(name=group_name).exists()

    @staticmethod
    def add_user_to_group(user: User, group_name: str) -> None:
        group = models.Group.objects.get(name=group_name)
        user.groups.add(group)
        group.user_set.add(user)

    @staticmethod
    def remove_user_from_group(user: User, group_name: str) -> None:
        group = models.Group.objects.get(name=group_name)
        user.groups.remove(group)
        group.user_set.remove(user)

    @staticmethod
    def make_user_mod(user: User) -> None:
        UserService.add_user_to_group(user, "Asset Moderator")
        UserService.remove_user_from_group(user, "Asset User")

    @staticmethod
    def make_user_admin(user: User) -> None:
        UserService.add_user_to_group(user, "Asset Admin")
        UserService.remove_user_from_group(user, "Asset User")

    @staticmethod
    def filter_user(**conditions) -> QuerySet:
        return get_user_model().objects.filter(**conditions)






