from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny

from apps.core.views import HealthView

schema_view = SpectacularAPIView.as_view(authentication_classes=[], permission_classes=[AllowAny])
docs_view = SpectacularSwaggerView.as_view(
    url_name="schema",
    authentication_classes=[],
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("health", HealthView.as_view(), name="health"),
    path("api/v1/", include("apps.identity.urls")),
    path("api/v1/", include("apps.transactions.urls")),
    path("api/v1/", include("apps.rules.urls")),
    path("api/v1/", include("apps.alerts.urls")),
    path("api/v1/", include("apps.audit.urls")),
    path("api/schema/", schema_view, name="schema"),
    path("api/docs/", docs_view, name="docs"),
]
