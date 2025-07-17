import django_filters

from .models import Ad


class AdsFilter(django_filters.FilterSet):
    """
    The filter for fields title and description of ad
    """

    class Meta:
        model = Ad
        fields = {"title": ["icontains"], "description": ["icontains"]}
