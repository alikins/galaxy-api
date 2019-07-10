# (c) 2012-2019, Ansible by Red Hat
#
# This file is part of Ansible Galaxy
#
# Ansible Galaxy is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by
# the Apache Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Ansible Galaxy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Apache License for more details.
#
# You should have received a copy of the Apache License
# along with Galaxy.  If not, see <http://www.apache.org/licenses/>.


from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import semantic_version

from galaxy_api.api import base
from galaxy_api.api import models
from galaxy_api.api.v3 import serializers
# from galaxy_api.api.v1.pagination import DefaultPagination


__all__ = (
    'VersionDetailView',
    'VersionListView',
    'CollectionArtifactView',
)


class VersionDetailView(base.RetrieveUpdateDestroyAPIView):
    # model = models.CollectionVersion
    permission_classes = (AllowAny, )
    serializer_class = serializers.VersionDetailSerializer

    def get(self, request, *args, **kwargs):
        """Return a collection version."""
        return Response({'not_implemented': 'yet'})
        # version = self._get_version()
        # serializer = serializers.VersionDetailSerializer(
        #     version, context={'request': self.request})
        # return Response(serializer.data)

    def _get_version(self):
        """
        Get collection version from either version id, or from
        collection namespace, collection name, and version string.
        """
        version_pk = self.kwargs.get('version_pk', None)
        version_str = self.kwargs.get('version', None)

        # TODO/FIXME(akl): implement with pulp_ansible client

    def _get_collection(self):
        """Get collection from namespace and name."""
        ns_name = self.kwargs.get('namespace', None)
        name = self.kwargs.get('name', None)
        # raise 404Exception('Not implemented yet')
        return Response({'not_implemented': 'yet'})


class VersionListView(base.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = serializers.VersionSummarySerializer
    # pagination_class = DefaultPagination

    def list(self, request, *args, **kwargs):
        """Override drf ListModelMixin to sort versions by semver."""

        return Response({'not_implemented': 'yet'})

    def _get_collection(self):
        """Get collection from either id, or namespace and name."""
        # pk = self.kwargs.get('pk', None)
        # if pk:
        #    return get_object_or_404(models.Collection, pk=pk)

        ns_name = self.kwargs.get('namespace', None)
        name = self.kwargs.get('name', None)

        return Response({'not_implemented': 'yet'})


# TODO(cutwater): Whith #1858 this view is considered for removal.
class CollectionArtifactView(base.RetrieveAPIView):
    permission_classes = (AllowAny, )
    serializer_class = serializers.CollectionArtifactSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Response({'not_implemented': 'yet'})
