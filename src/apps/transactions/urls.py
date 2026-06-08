from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.transactions.api.views import TransactionViewSet

router = DefaultRouter()
router.register(r"transactions", TransactionViewSet, basename="transactions")

urlpatterns = [
    path("", include(router.urls)),
]
