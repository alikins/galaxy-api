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

# app_name = 'api'
    path('test', TestView.as_view(), name='test')
        path('collections/<int:pk>/',
        CollectionDetailView.as_view(),
        name='collection-detail'),
    path('ping', PingView.as_view()),
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
]
