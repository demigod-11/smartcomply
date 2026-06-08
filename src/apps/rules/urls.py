from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.rules.api.views import RuleViewSet

router = DefaultRouter()
router.register(r"rules", RuleViewSet, basename="rules")

urlpatterns = [
    path("", include(router.urls)),
]
