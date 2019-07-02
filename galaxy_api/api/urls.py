
from django.conf import settings
from django.urls import include, path, re_path

from galaxy_api.api.views import ApiRootView
prefix = settings.API_PATH_PREFIX

app_name = 'api'
urlpatterns = [
    re_path(r'^$', ApiRootView.as_view(), name='api_root_view'),

    path('v1/', include('galaxy_api.api.v1.urls',
                        namespace='v1'
                        )),
    path('v2/', include('galaxy_api.api.v2.urls',
                        namespace='v2'
                        )),

]
