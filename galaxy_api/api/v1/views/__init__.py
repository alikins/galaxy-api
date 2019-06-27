<<<<<<< HEAD
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .collection import CollectionDetailView, CollectionListView
from .collection_version import VersionDetailView, VersionListView
||||||| merged common ancestors
from .ping import PingView
from .collection import CollectionDetailView, CollectionListView
from .collection_version import VersionDetailView, VersionListView
=======
from .ping import PingView
>>>>>>> WIP, oops, mv collections to v2/

__all__ = (
    'TestView'
    'CollectionDetailView'
    'CollectionListView',
    'VersionDetailView',
    'VersionListView',
)


class TestView(APIView):
    def get(self, request):
        return Response({
            '_href': reverse('api:v1:test'),
            'status': 'OK',
        })
