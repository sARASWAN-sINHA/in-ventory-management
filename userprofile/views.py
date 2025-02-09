from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import Profile
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
                "message": "Profile created successfully.",
                "detail": "Profile for the user who raised the request has been created successfully.",
                "status": status.HTTP_201_CREATED,
                "data": profile.validated_data,
            }
            return Response(data=data, status=status.HTTP_201_CREATED)

        except Exception as e:
            data = {
                "message": "Profile creation failed.",
                "detail": f"{e}",
                "status": status.HTTP_400_BAD_REQUEST,
                "data": profile.errors,
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, profile):
        profile.save(user=self.request.user)






