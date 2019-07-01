from django.urls import path

from .views import TestView

from .views import PingView
from .views import (
    NamespaceList,
    NamespaceDetail,
    NamespaceProviderNamespacesList,
)

from .views import (
    ProviderNamespaceList,
    ProviderNamespaceDetail,
)
from .views import (
    ProviderNamespaceList,
    ProviderNamespaceDetail,
)

from .views import (
    ProviderSourceList,
)

from .views import (
    UserList,
    UserDetail,
    ActiveUserView,
)

app_name = 'api'
urlpatterns = [
    path('test', TestView.as_view(), name='test')
        path('collections/<int:pk>/',
        CollectionDetailView.as_view(),
        name='collection-detail'),

    path('namespaces', NamespaceList.as_view(), name='namespace_list'),
    path('namespaces/<int:pk>/',
         NamespaceDetail.as_view(),
         name='namespace_detail'),

    path('namespaces/<int:pk>/provider_namespaces/',
         NamespaceProviderNamespacesList.as_view(),
         name='namespace_provider_namespaces_list'),


    path('provider_namespaces',
         ProviderNamespaceList.as_view(),
         name='provider_namespace_list'),
    path('provider_namespaces/<int:pk>/',
         ProviderNamespaceDetail.as_view(),
         name='provider_namespace_detail'),

    path('providers/sources/',
         ProviderSourceList.as_view(),
         name='provider_source_list'),

    path('users',
         UserList.as_view(),
         name='user_list'),

    path('users/<int:pk>',
         UserDetail.as_view(),
         name='user_detail'),

    # if False:
    #     user_urls = [
    #         url(r'^$', views.UserList.as_view(), name='user_list'),
    #         url(r'^(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user_detail'),
    #         # url(r'^(?P<pk>[0-9]+)/token/$',
    #         #     views.UserTokenView.as_view(),
    #         #     name='user_token_view')
    #     ]


]
