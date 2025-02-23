
from rest_framework import serializers
from rest_framework import status

from core.models import Profile
from core.services.users import UserService

from djoser.serializers import UserSerializer

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "designation",
            "qualification",
            "phone_number",
            "address",
        )


    def validate_first_name(self, value):
        if value is None or value == "":
            raise serializers.ValidationError("First name is required.")
        return value

    def validate_designation(self, value):
        if  value is None or value == "":
            raise serializers.ValidationError("Designation is required.")
        return value
class CustomUserSerialzer(UserSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta(UserSerializer.Meta):
        fields = ("id", "email", "is_active", "is_staff", "is_superuser", "profile")
        read_only_fields = ("email", "is_active", "is_staff", "is_superuser", "profile")


class SetUserRoleSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_user_email(self, value):
        if not UserService.get_user_by_id(value):
            raise serializers.ValidationError("User does not exist.", code=status.HTTP_404_NOT_FOUND)
        return value
