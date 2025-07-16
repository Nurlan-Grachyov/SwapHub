from rest_framework.routers import DefaultRouter

from change.apps import ChangeConfig
from change.views import ChangeViewSet

app_name = ChangeConfig.name
router = DefaultRouter()
router.register(r"change", ChangeViewSet, basename="change")

urlpatterns = [] + router.urls
