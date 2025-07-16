import django_filters

from .models import Product


class AdsFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {"title": ["icontains"], "description": ["icontains"]}
