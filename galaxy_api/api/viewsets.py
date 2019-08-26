
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from django.urls import reverse


class ApiRootViewset(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    view_name = 'REST API'

    def retrieve(self, request, *args, **kwargs):
        # list supported API versions
        current = reverse('api:v3:api_view', args=[])
        data = dict(
            description='Automation Hub REST API',
            current_version='v3',
            available_versions=dict(
                v3=current,
            ),
        )
        return Response(data)
