from django.urls import path

from .views import TestView
from .views import CollectionDetailView
from .views import CollectionDetailView, CollectionListView
from .views import VersionDetailView, VersionListView


app_name = 'api'
urlpatterns = [
    path('test', TestView.as_view(), name='test')
        path('collections/<int:pk>/',
        CollectionDetailView.as_view(),
        name='collection-detail'),
    path('collections/',
         CollectionListView.as_view(),
         name='collection-list'),
    path('collections/<int:pk>/',
         CollectionDetailView.as_view(),
         name='collection-detail'),
    path('collections/<str:namespace>/<str:name>/',
         CollectionDetailView.as_view(),
         name='collection-detail'),

    path('collection-versions/<int:version_pk>/',
         VersionDetailView.as_view(),
         name='version-detail'),
    path('collections/<str:namespace>/<str:name>/versions/<str:version>/',
         VersionDetailView.as_view(),
         name='version-detail'),

    # Collection Version list URLs
    path('collections/<int:pk>/versions/',
         VersionListView.as_view(),
         name='version-list'),
    path('collections/<str:namespace>/<str:name>/versions/',
         VersionListView.as_view(),
         name='version-list'),
]
