from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.alerts.api.views import AlertViewSet

router = DefaultRouter()
router.register(r"alerts", AlertViewSet, basename="alerts")

urlpatterns = [
    path("", include(router.urls)),
]
