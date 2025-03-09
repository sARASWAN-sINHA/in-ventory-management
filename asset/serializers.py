from rest_framework import serializers

from core.models import Asset, AssetType, AssetFileUploadHistory
from userprofile.serializers import CustomUserSerialzer


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = ("id", "type", "sub_type", "group", "description", "code")


class AssetSerializer(serializers.ModelSerializer):

    asset_type = AssetTypeSerializer(read_only=True)
    asset_type_id = serializers.IntegerField(write_only=True)

    current_owner = CustomUserSerialzer(read_only=True)

    class Meta:
        model = Asset
        fields = (
            "id",
            "name",
            "description",
            "quantity",
            "location",
            "manufacturer",
            "current_owner",
            "asset_type",
            "asset_type_id",
        )

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr.get("asset_type").pop("id")
        return repr



class RequisitionSerialzier(serializers.ListField):
        asset_id=serializers.IntegerField()
        quantity=serializers.IntegerField()
        start_date=serializers.DateTimeField()
        end_date=serializers.DateTimeField()

class AssetAssignSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    requisitions = RequisitionSerialzier()


class AssetTypeGetCode(serializers.ModelSerializer):
     class Meta:
        model = AssetType
        fields = ("type", "sub_type", "group",)



class AssetFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetFileUploadHistory
        fields = ["uploaded_file",]

class AssetValidatedFileUploadSerialzier(serializers.ModelSerializer):
    uploaded_at = serializers.DateTimeField(read_only=True)
    uploaded_by = CustomUserSerialzer(read_only=True)
    class Meta:
        model = AssetFileUploadHistory
        fields = ["uploaded_file", "validated_file", "uploaded_at", "uploaded_by"]

