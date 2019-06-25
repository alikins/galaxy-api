from django.shortcuts import get_object_or_404

from rest_framework import exceptions as exc
from rest_framework.response import Response
from rest_framework import status as http_codes
from rest_framework.views import APIView

from galaxy_common import models
from galaxy_api.api.v1 import serializers

__all__ = (
    'CollectionView'
)


class CollectionDetailView(APIView):
    # permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        """Return a collection."""
        collection = self._get_collection()
        serializer = serializers.CollectionSerializer(
            collection, context={'request': request})
        return Response(serializer.data)

    def _get_collection(self):
        """Get collection from either id, or namespace and name."""
        pk = self.kwargs.get('pk', None)
        ns_name = self.kwargs.get('namespace', None)
        name = self.kwargs.get('name', None)

        if pk:
            return get_object_or_404(models.Collection, pk=pk)
        ns = get_object_or_404(models.Namespace, name=ns_name)
        return get_object_or_404(models.Collection, namespace=ns, name=name)
