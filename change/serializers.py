from rest_framework import serializers

from change.models import ExchangeOffer
from django.utils.translation import gettext_lazy as _


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeOffer
        fields = "__all__"

    def validate(self, attrs):
        if attrs.get('ad_sender') == attrs.get('ad_receiver'):
            raise serializers.ValidationError(_("Объявление отправителя и получателя не должны совпадать."))

        if attrs.get('sender_user') == attrs.get('receiver_user'):
            raise serializers.ValidationError(_("Отправитель и получатель не должны совпадать."))

        return attrs
