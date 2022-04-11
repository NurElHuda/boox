from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(title="Boox API", default_version="v1", description="",),
    public=True,
    permission_classes=(),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('boox_app.urls')),
    path('favicon.ico', RedirectView.as_view(url="/static/favicon.ico", permanent=True)),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    )
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
