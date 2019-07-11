from django.urls import path

from .views import TestView

from .views import (
    CollectionDetailView,
    CollectionListView,
)

from .views import (
    NamespaceList,
    NamespaceDetail,
)


from .views import (
    UserList,
    UserDetail,
    # ActiveUserView,
)

app_name = 'api'
urlpatterns = [
    path('test', TestView.as_view(), name='test'),

    path('namespaces', NamespaceList.as_view(), name='namespace_list'),
    path('namespaces/<int:pk>/',
         NamespaceDetail.as_view(),
         name='namespace_detail'),

    path('users',
         UserList.as_view(),
         name='user_list'),

    path('users/<int:pk>',
         UserDetail.as_view(),
         name='user_detail'),

    # TODO/FIXME(akl) - these views will be
    # implemented as a client against pulp API
    
    path('collections/',
         CollectionListView.as_view(),
         name='collection-list'),

    # path('collections/<int:pk>/',
    #      CollectionDetailView.as_view(),
    #      name='collection-detail'),

    path('collections/<str:namespace>/<str:name>/',
         CollectionDetailView.as_view(),
         name='collection-detail'),

    # path('collection-versions/<int:version_pk>/',
    #      VersionDetailView.as_view(),
    #      name='version-detail'),
    # path('collections/<str:namespace>/<str:name>/versions/<str:version>/',
    #      VersionDetailView.as_view(),
    #      name='version-detail'),

    # # Collection Version list URLs
    # path('collections/<int:pk>/versions/',
    #      VersionListView.as_view(),
    #      name='version-list'),
    # path('collections/<str:namespace>/<str:name>/versions/',
    #      VersionListView.as_view(),
    #      name='version-list'),
]
