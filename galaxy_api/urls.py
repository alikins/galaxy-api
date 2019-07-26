"""URLs Configuration."""

from django.conf import settings
from django.urls import include, path

from rest_framework.schemas import get_schema_view

api_prefix = settings.API_PATH_PREFIX.strip('/')
urlpatterns = [
    path(f'{api_prefix}/', include('galaxy_api.api.urls', namespace='api')),

    path('openapi',
         get_schema_view(title="Your Project",
                         description="API for all things …"),
         name='openapi-schema'),
]
