from rest_framework import serializers

from ads.models import Product


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        product = Product.objects.create(user=user, **validated_data)
        return product