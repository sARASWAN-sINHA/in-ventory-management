from datetime import datetime
import os
from django.conf import settings
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser as IsSuperUser
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser

from core.models import AssetType, Asset
from core.permissions import IsAssetAdmin, IsAssetModerator
from core.services.assets import AssetService
from core.services.files import FileService
from core.services.users import UserService
from core.messages import (
    response_bad_request,
    response_created,
    response_not_found,
    response_ok,
    response_server_error,
    response_list,
)
from core.exceptions import (
    raise_400_exception,
    raise_403_exception,
    raise_404_exception,
)

from .serializers import (
    AssetAssignSerializer,
    AssetSerializer,
    AssetTypeGetCode,
    AssetTypeSerializer,
    AssetFileUploadSerializer,
)

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponse


from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend


class AssetTypeViewSet(ModelViewSet):
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("type", "sub_type", "group",)
    filterset_fields = ("type", "sub_type", "group",)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, (IsAssetAdmin | IsSuperUser)]
        elif self.action in ["list", "retrieve"]:
            self.permission_classes = [
                IsAuthenticated,
                (IsAssetModerator | IsAssetAdmin | IsSuperUser),
            ]
        return super().get_permissions()


    @extend_schema(
        request=AssetTypeGetCode,
        summary="Gets the asset-code",
        description="Fetches the asset code of the corresponding type, sub-type, group",
    )
    @action(
        detail=False,
        methods=["POST"],
        url_path="code",
        permission_classes=[
            IsAuthenticated,
            (IsAssetModerator | IsAssetAdmin | IsSuperUser),
        ],
    )
    def get_code(self, request):
        seriallized_request = AssetTypeGetCode(data=request.data)
        seriallized_request.is_valid(raise_exception=True)

        type = seriallized_request.validated_data.get("type")
        sub_type = seriallized_request.validated_data.get("sub_type")
        group = seriallized_request.validated_data.get("group")

        asset_type = AssetType.objects.filter(
            Q(type__exact=type), Q(sub_type__exact=sub_type), Q(group__exact=group)
        ).first()

        if asset_type is None:
            return response_not_found(
                detail="Access code for the given type, subtype, and group not found!",
                data={},
            )
        return response_ok(detail="Access code found.", data={"asset_code": asset_type.code})


class AssetViewSet(ModelViewSet):
    serializer_class = AssetSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_filter = (
        "location",
        "manufacturer",
        "current_owner",
        "asset_type__type",
        "asset_type__sub_type",
        "asset_type__group",
        "asset_type__code",
    )
    ordering_filter = (
        "quantity",
        "current_owner",
        "location",
        "manufacturer",
        "asset_type__type",
        "asset_type__sub_type",
        "asset_type__group",
        "asset_type__code",

    )
    filterset_fields = (
        "location",
        "manufacturer",
        "current_owner",
        "asset_type",
        "quantity",
    )

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [
                IsAuthenticated,
                (IsAssetModerator | IsAssetAdmin | IsSuperUser),
            ]
        elif self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_object(self):
        asset = get_object_or_404(Asset, pk=self.kwargs.get("pk"))
        if UserService.is_user_in_group(self.request.user, "Asset User"):
            if asset.current_owner == self.request.user:
                return asset
            else:
                raise_403_exception(
                    detail="You are not allowed to perform this action."
                )
        return asset

    def get_queryset(self):
        if UserService.is_user_in_group(self.request.user, "Asset User"):
            return Asset.objects.filter(current_owner=self.request.user).order_by(
                "-quantity"
            )
        return Asset.objects.all().order_by("-quantity")

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not AssetService.check_qunatity_greater_than_zero(
            serializer.validated_data.get("quantity")
        ):
            raise_400_exception("Quantity must be greater than 0")

        if UserService.filter_user(is_superuser=True).exists():
            serializer.save(
                current_owner=UserService.filter_user(is_superuser=True).first()
            )
        else:
            return response_server_error(
                detail="No superuser found to assign the asset to.", data={}
            )
        return response_created(
            detail="Asset created successfully", data=serializer.data
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response_list(
            detail="Assets retrieved successfully.",
            data=response.data,
            count=self.get_queryset().count(),
        )

    @extend_schema(
        request=AssetAssignSerializer,
        responses={200: {"detail": "Assets assigned successfully"}},
        summary="Assign assets to a user",
        description="Assign assets to a user by providing the user's email and the asset IDs",
    )
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAuthenticated, (IsAssetAdmin | IsAssetModerator) | IsSuperUser],
    )
    def assign(self, request):

        serialized_request_data = AssetAssignSerializer(data=request.data)
        serialized_request_data.is_valid(raise_exception=True)

        user_id = serialized_request_data.validated_data.get("user_id")
        requisitions = serialized_request_data.validated_data.get("requisitions")

        user = UserService.get_user_by_id(user_id)

        if user == "User not found":
            raise_404_exception(detail=f"User with id: {user_id} not found!")

        validation_success, validation_result = AssetService.validate_requisitions(requisitions)
        print(validation_success, validation_result)

        if validation_success is True:
            AssetService.assign(user, validation_result)
            return response_ok(detail="Asset(s) assigned to user succesfully!", data={})
        else:
            validation_errors = validation_result.get("validation_errors", [])
            quantity_validation_errors = validation_result.get("quantity_validation_errors", [])
            date_validation_error = validation_result.get("date_validation_error", [])
            error_mssgs = []

            print(validation_errors, quantity_validation_errors, date_validation_error)

            if len(validation_errors):

                error_mssgs +=list(
                        map(
                            lambda x: f"{x[1]}: {x[0]}",
                            validation_errors,
                        )
                    ),
            if len(quantity_validation_errors):

                error_mssgs += list(
                    map(
                        lambda x: f"{x[1]}: {x[0]}",
                        quantity_validation_errors,
                    )
                )

            if len(date_validation_error):
                error_mssgs += list(
                    map(
                        lambda x: f"{x[1]}: {x[0]}",
                        date_validation_error,
                    )
                )

            return response_bad_request(
                detail="Invalid requisition values.", data=error_mssgs
            )


class AssetFileViewSet(ViewSet):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsSuperUser | IsAssetAdmin]

    @action(detail=False, methods=["GET"], url_path="template/download")
    def download_template_file(self, request):
        response = None
        filename = "template.csv"
        try:
            file = FileService.download_template_file()
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = f"attachment; filename={filename};"
            file.to_csv(response, index=False)
        except Exception as e:
            response = response_bad_request(detail=str(e), data={})
        return response

    @action(detail=False, methods=["POST"], url_path="upload")
    def upload_file(self, request):

        serializer = AssetFileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data.get("uploaded_file")

        validation_status, updated_file_df, totality_check, totality_check_error_messages = FileService.validate_file(uploaded_file)

        file_path = FileService.generate_file_path(request.user.email, uploaded_file)

        #[TODO] Change this to excel.
        #[TODO] ADD A NEW SHEET IN THE EXCEL FILE WITH THE "totality_check_error_messages", IF ANY.
        updated_file_df.to_csv(file_path, index=False)

        serialized_instance = serializer.save(uploaded_by=request.user, validated_file=file_path)

        print(f"File upload by {self.request.user.email} at {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')} recorded at {serialized_instance.uploaded_file.path}!")

        if validation_status:
            #
            # [TODO] Subtract qunatities from assets.
            #

            return response_ok(
                detail="File validated succesfully. Qunatities updated.",
                data=serialized_instance.uploaded_file.path,
            )
        else:
            return response_bad_request(
                detail=f"File validation failed.",
                data={"message": "Please check the log csv files for more details.. "},
            )
