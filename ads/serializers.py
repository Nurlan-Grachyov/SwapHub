from rest_framework import serializers

from ads.models import Product


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
