
from rest_framework import serializers

from core.models import Profile
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
        fields = ("email", "is_active", "is_staff", "is_superuser", "profile")
        read_only_fields = ("email", "is_active", "is_staff", "is_superuser", "profile")

