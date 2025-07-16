import django_filters

from .models import ExchangeOffer


class ChangeFilter(django_filters.FilterSet):
    class Meta:
        model = ExchangeOffer
        fields = {"comment": ["icontains"]}
