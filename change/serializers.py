from rest_framework import serializers

from change.models import ExchangeOffer


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeOffer
        fields = "__all__"
        read_only_fields = [
            "ad_sender",
            "ad_receiver",
            "sender_user",
            "receiver_user",
            "comment",
            "created_at",
            "updated_at",
        ]
