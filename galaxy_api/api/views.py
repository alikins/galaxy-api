from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.urls import reverse
from galaxy_api.api import base


class ApiRootView(base.APIView):
    permission_classes = (AllowAny,)
    view_name = 'REST API'

    def get(self, request, format=None):
        # list supported API versions
        current = reverse('api:api_root_view', args=[])
        data = dict(
            description='GALAXY REST API',
            current_version='v1',
            available_versions=dict(
                v1=current,
                v2='/api/v2/',
            ),
            stuff='blippy'
        )
        return Response(data)
