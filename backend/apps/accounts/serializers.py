from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "display_name",
            "email",
            "rating_estimate",
            "board_orientation_hint",
            "is_staff",
        )
        read_only_fields = ("id", "username", "email", "is_staff")
