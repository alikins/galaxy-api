
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.urls import reverse
from galaxy_api.api import base


class ApiV2RootView(base.APIView):
    permission_classes = (AllowAny,)
    view_name = 'REST API'

    def get(self, request, format=None):
        # list supported API versions
        # current = reverse('api:api_root_v2_view', args=[])
        data = dict(
            description='GALAXY REST API',
            stuff='blippy v2'
        )
        return Response(data)
