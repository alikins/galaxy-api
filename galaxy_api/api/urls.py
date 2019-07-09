
from django.conf import settings
from django.urls import include, path, re_path

from galaxy_api.api.views import ApiRootView
prefix = settings.API_PATH_PREFIX

app_name = 'api'
urlpatterns = [
    re_path(r'^$', ApiRootView.as_view(), name='api_root_view'),

    path('v3/', include('galaxy_api.api.v3.urls',
                        namespace='v4'
                        )),

]
