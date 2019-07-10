from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .namespace import (
    NamespaceList,
    NamespaceDetail,
    NamespaceProviderNamespacesList,
    # NamespaceContentList
)

from .provider_namespace import (
    ProviderNamespaceList,
    ProviderNamespaceDetail,
    # ProviderNamespaceRepositoriesList,
)

from .provider_source import (
    ProviderSourceList
)

from .users import (
    UserDetail,
    UserList,
    ActiveUserView,
)

from .collection import (
    CollectionDetailView,
    CollectionListView,
)

from .collection_version import (
    VersionDetailView,
    VersionListView,
)

__all__ = (
    'ActiveUserView',

    'CollectionDetailView',
    'CollectionListView',

    'NamespaceList',
    'NamespaceDetail',
    'NamespaceProviderNamespacesList',
    # 'NamespaceContentList',

    'ProviderNamespaceList',
    'ProviderNamespaceDetail',
    # 'ProviderNamespaceRepositoriesList',

    'ProviderSourceList',

    'TestView',

    'UserDetail',
    'UserList',

)


class TestView(APIView):
    def get(self, request):
        return Response({
            '_href': reverse('api:v3:test'),
            'status': 'OK',
        })
