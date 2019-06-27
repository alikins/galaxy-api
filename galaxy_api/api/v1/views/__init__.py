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

__all__ = (
    'TestView'
    'NamespaceList',
    'NamespaceDetail',
    'NamespaceProviderNamespacesList',
    # 'NamespaceContentList',
    'ProviderNamespaceList',
    'ProviderNamespaceDetail',
    # 'ProviderNamespaceRepositoriesList',
    'ProviderSourceList',
)


class TestView(APIView):
    def get(self, request):
        return Response({
            '_href': reverse('api:v1:test'),
            'status': 'OK',
        })
