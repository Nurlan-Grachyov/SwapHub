from rest_framework import serializers

from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """
    The serializer of a registration with the method of a creating
    """

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        """
        The account creation method
        """

        user = CustomUser(
            email=validated_data["email"], username=validated_data.get("username")
        )
        user.set_password(validated_data["password"])
        user.is_active = True
        user.save()
        return user
