from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser as IsSuperUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from core.models import Profile
from core.permissions import IsAssetAdmin, IsAssetModerator
from core.services.users import UserService
from core.messages import (
    response_ok,
    response_created,
    response_bad_request,
)

from .serializers import ProfileSerializer, SetUserRoleSerializer


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        profile = self.serializer_class(data=request.data)
        try:
            profile.is_valid(raise_exception=True)
            profile.save(user=self.request.user)

            return response_created(
                message="Profile created successfully.",
                detail="Profile for the user who raised the request has been created successfully.",
                data=profile.validated_data,
            )

        except Exception as e:
            return response_bad_request(
                message="Profile creation failed.",
                detail=f"{e}",
                data=profile.error_messages,
            )


class SetUserToGroupView(ViewSet):

    serializer_class = (SetUserRoleSerializer,)

    @action(
        detail=False,
        methods=["GET"],
        url_path="mod",
        permission_classes=[
            IsAuthenticated,
            (IsAssetAdmin | IsAssetModerator) | IsSuperUser,
        ],
    )
    def set_user_to_mod(self, request):

        serialized_request = self.serializer_class(data=request.data)
        serialized_request.is_valid(raise_exception=True)
        user_id = serialized_request.data.get("id")

        user = UserService.get_user_by_id(user_id)

        if UserService.is_user_in_group(user, "Asset Moderator"):
            return response_bad_request(
                message="Cannot add user to Moderator group.",
                detail="The user is already a moderator.",
                data={},
            )

        if UserService.is_user_in_group(user, "Asset Admin"):
            return response_bad_request(
                message="Cannot add user to Admin group.",
                detail="The user is an admin. Cannot set an admin as a moderator.",
                data={},
            )

        UserService.make_user_mod(user)

        return response_ok(
            message="User added to Moderator group.",
            detail="The user has been set as a moderator successfully.",
            data={},
        )

    @action(
        detail=False,
        methods=["GET"],
        url_path="admin",
        permission_classes=[IsAuthenticated, IsAssetAdmin | IsSuperUser],
    )
    def set_uset_to_admin(self, request):

        serialized_request = self.serializer_class(data=request.data)
        serialized_request.is_valid(raise_exception=True)
        user_id = serialized_request.validated_data.get("id")

        user = UserService.get_user_by_id(user_id)

        if UserService.is_user_in_group(user, "Asset Admin"):
            return response_bad_request(
                message="Cannot add user to Admin group.",
                detail="The user is already an admin.",
                data={},
            )

        UserService.make_user_admin(user)

        if UserService.is_user_in_group(user, "Asset Moderator"):
            UserService.remove_user_from_group(user, "Asset Moderator")

        return response_ok(
            message="User added to Admin group.",
            detail="The user has been set as a admin successfully.",
            data={},
        )
