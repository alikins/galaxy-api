from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .collection import CollectionDetailView, CollectionListView

__all__ = (
    'TestView'
    'CollectionDetailView'
    'CollectionListView',
)


class TestView(APIView):
    def get(self, request):
        return Response({
            '_href': reverse('api:v1:test'),
            'status': 'OK',
        })
