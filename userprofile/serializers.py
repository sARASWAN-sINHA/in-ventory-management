
from rest_framework import serializers

from core.models import Profile
from djoser.serializers import UserSerializer

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "designation",
            "qualification",
            "phone_number",
            "address",
            "user",
        )


    def validate_first_name(self, value):
        if value is None or value == "":
            raise serializers.ValidationError("First name is required.")
        return value

    def validate_designation(self, value):
        if  value is None or value == "":
            raise serializers.ValidationError("Designation is required.")
        return value

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr["username"] = instance.user.email
        return repr

