"""API v3 URLs Configuration."""

from django.urls import path

from . import viewsets


app_name = 'api'
urlpatterns = [
    path('', viewsets.ApiV3Viewset.as_view({'get': 'retrieve'}), name='api_root_view'),
    path(
        'collections/',
        viewsets.CollectionViewSet.as_view({'get': 'list'}),
    ),
    path(
        'collections/<str:namespace>/<str:name>/',
        viewsets.CollectionViewSet.as_view({'get': 'retrieve'}),
    ),
    path(
        'collections/<str:namespace>/<str:name>/versions/',
        viewsets.CollectionVersionViewSet.as_view({'get': 'list'}),
    ),
    path(
        'collections/<str:namespace>/<str:name>/versions/<str:version>/',
        viewsets.CollectionVersionViewSet.as_view({'get': 'retrieve'}),
    ),
    path(
        'artifacts/collections/',
        viewsets.CollectionArtifactViewSet.as_view({'post': 'upload'}),
    ),
    path(
        'artifacts/collections/<str:filename>',
        viewsets.CollectionArtifactViewSet.as_view({'get': 'download'}),
    ),
]
