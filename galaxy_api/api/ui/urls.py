from django.urls import path, include
from rest_framework import routers

from . import viewsets


router = routers.SimpleRouter()
router.register('namespaces', viewsets.NamespaceViewSet)
router.register('collections', viewsets.CollectionViewSet, basename='collections')
router.register(
    'collections/(?P<collection>{})/versions'.format(
        viewsets.CollectionViewSet.lookup_value_regex
    ),
    viewsets.CollectionVersionViewSet,
    basename='collection-versions',
)
router.register(
    'imports/collections',
    viewsets.CollectionImportViewSet,
    basename='collection-imports')

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]
