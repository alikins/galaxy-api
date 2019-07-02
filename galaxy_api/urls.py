"""URLs Configuration."""

from django.conf import settings
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


api_prefix = settings.API_PATH_PREFIX.strip('/')

api_info = openapi.Info(
      title="GalaxyApi",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="alikins@redhat.com"),
      license=openapi.License(name="GPL3"),
   )

schema_view = get_schema_view(
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(f'{api_prefix}/', include('galaxy_api.api.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
