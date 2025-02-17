from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from core.models import Profile
from core.permissions import IsAssetAdmin, IsAssetModerator
from core.services.users import UserService
from .serializers import ProfileSerializer



class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """
    A viewset for retrieving, updating, and creating user profiles.
    Attributes:
        serializer_class (ProfileSerializer): The serializer class used for profile data.
        queryset (QuerySet): The queryset containing all profile objects.
        permission_classes (list): The list of permission classes required to access this viewset.
    Methods:
        create(request, *args, **kwargs):
            Handles the creation of a new user profile.
            Args:
                request (Request): The request object containing profile data.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.
            Returns:
                Response: A response object with a success or failure message and status code.
        perform_create(profile):
            Saves the profile instance with the associated user.
            Args:
                profile (ProfileSerializer): The profile serializer instance to be saved.
    """

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        profile = self.serializer_class(data=request.data)
        try:
            profile.is_valid(raise_exception=True)
            self.perform_create(profile)

            data = {
                "status": status.HTTP_201_CREATED,
                "message": "Profile created successfully.",
                "detail": "Profile for the user who raised the request has been created successfully.",
                "data": profile.validated_data,
            }
            return Response(data=data, status=status.HTTP_201_CREATED)

        except Exception as e:
            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Profile creation failed.",
                "detail": f"{e}",
                "data": profile.errors,
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, profile):
        profile.save(user=self.request.user)



class SetUserToGroupView(ViewSet):

    @action(detail=False, methods=["GET"], url_path="mod", permission_classes=[IsAuthenticated, (IsAssetAdmin | IsAssetModerator)])
    def set_user_to_mod(self, request):
        """
        Sets the user to moderator.
        Args:
            request (Request): The request object containing the user data.
        Returns:
            Response: A response object with a success or failure message and status code.
        """
        user = self.request.user

        if UserService.is_user_in_group(user, "Asset Moderator"):
            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Cannot add user to Moderator group.",
                "detail": "The user is already a moderator.",
            }

            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if UserService.is_user_in_group(user, "Asset Admin"):
            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Cannot add user to Admin group.",
                "detail": "The user is an admin. Cannot set an admin as a moderator.",
            }

            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        UserService.make_user_mod(user)

        data = {
            "status": status.HTTP_200_OK,
            "message": "User added to Moderator group.",
            "detail": "The user has been set as a moderator successfully.",
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="admin", permission_classes=[IsAuthenticated, IsAssetAdmin])
    def set_uset_to_admin(self, request):
        """
        Sets the user to admin.
        Args:
            request (Request): The request object containing the user data.
        Returns:
            Response: A response object with a success or failure message and status code.
        """
        user = self.request.user

        if UserService.is_user_in_group(user, "Asset Admin"):
            data = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Cannot add user to Admin group.",
                "detail": "The user is already an admin.",
            }

            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        UserService.make_user_admin(user)
        if UserService.is_user_in_group(user, "Asset Moderator"):
            UserService.remove_user_from_group(user, "Asset Moderator")

        data = {
            "status": status.HTTP_200_OK,
            "message": "User added to Admin group.",
            "detail": "The user has been set as an admin successfully.",
        }
        return Response(data=data, status=status.HTTP_200_OK)






