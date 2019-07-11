from django.shortcuts import get_object_or_404
from rest_framework import mixins as drf_mixins
from rest_framework.response import Response
from rest_framework import views
from galaxy_api.api import exceptions
from galaxy_api.api import base
from galaxy_api.api.v3 import serializers
from galaxy_api.api import models

__all__ = (
    'CollectionDetailView',
    'CollectionListView',
)


class CollectionExistsError(exceptions.ConflictError):
    default_detail = 'Collection already exists.'
    default_code = 'conflict.collection_exists'


class RepositoryNameError(exceptions.ConflictError):
    default_detail = 'Repository already uses namespace and name.'
    default_code = 'conflict.repository_name_conflict'


class ArtifactExistsError(exceptions.ConflictError):
    default_detail = 'Artifact already exists.'
    default_code = 'conflict.artifact_exists'


class ArtifactInvalidError(exceptions.ValidationError):
    default_detail = 'Artifact not a valid tar archive file.'
    default_code = 'invalid.artifact_invalid_tarfile'


class ArtifactMaxSizeError(exceptions.ValidationError):
    default_detail = 'Artifact exceeds maximum size.'
    default_code = 'invalid.artifact_exceeds_max_size'


class CollectionDetailView(base.RetrieveAPIView):
    model = models.Collection
    serializer_class = serializers.CollectionSerializer
    queryset = models.Collection.objects.all()

    def get(self, request, *args, **kwargs):
        ns_name = self.kwargs.get('namespace', None)
        name = self.kwargs.get('name', None)

        ns = get_object_or_404(models.Namespace, name=ns_name)
        return get_object_or_404(models.Collection, namespace=ns, name=name)



#    def get_object(self):
#        """Return a collection."""
#        return {'not_implemented': 'yet'}

class CollectionListView(base.ListCreateAPIView):
    model = models.Collection
    serializer_class = serializers.CollectionSerializer
    queryset = models.Collection.objects.all()