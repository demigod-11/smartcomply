from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.identity.api.views import ApiClientViewSet

router = DefaultRouter()
router.register(r"api-clients", ApiClientViewSet, basename="api-clients")

urlpatterns = [
    path("", include(router.urls)),
]
