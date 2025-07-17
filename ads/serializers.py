from rest_framework import serializers

from ads.models import Ad


class AdSerializer(serializers.ModelSerializer):
    """
    The serializer for Ad
    """

    class Meta:
        model = Ad
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        product = Ad.objects.create(user=user, **validated_data)
        return product
