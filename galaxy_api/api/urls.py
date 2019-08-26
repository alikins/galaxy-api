"""API URLs Configuration."""

from django.urls import include, path

from .viewsets import ApiRootViewset
from .ui import urls as ui_urls
from .v3 import urls as v3_urls


app_name = 'api'
urlpatterns = [
    path('', ApiRootViewset.as_view({'get': 'retrieve'}), name='api_root_view'),
    path('v3/', include(v3_urls, namespace='v3')),
    path('v3/_ui/', include(ui_urls, namespace='ui')),
]
