from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser as IsSuperUser
from rest_framework.response import Response
from rest_framework import status

from core.models import AssetType, Asset
from core.permissions import IsAssetAdmin, IsAssetModerator
from core.services.users import UserService

from .serializers import AssetSerializer, AssetTypeSerializer


class AssetTypeViewSet(ModelViewSet):
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, (IsAssetAdmin | IsSuperUser)]
        elif self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class AssetViewSet(ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [
                IsAuthenticated,
                (IsAssetModerator | IsAssetAdmin | IsSuperUser),
            ]
        elif self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        if UserService.is_user_in_group(self.request.user, "Asset User"):
            return self.queryset.filter(current_owner=self.request.user)
        return self.queryset

    def create(self, request, *args, **kwargs):

        if int(request.data.get("quantity")) < 1:
            raise ValueError(
                detail={"quantity": "Quantity must be greater than 0"},
                code=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(current_owner=request.user)

        return Response(
            {
                "detail": "Asset created successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        assets = self.get_queryset()
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "detail": "Assets retrieved successfully",
                "count": assets.count(),
                "data": response.data,
            },
            status=status.HTTP_200_OK,
        )
