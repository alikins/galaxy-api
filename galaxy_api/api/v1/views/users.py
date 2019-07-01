import logging

from rest_framework import exceptions

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from galaxy_common import models

from galaxy_api.api import base as base_views
from galaxy_api.api.v1 import serializers


__all__ = [
    'UserList',
    'UserDetail',
    'ActiveUserView',
]

logger = logging.getLogger(__name__)

User = get_user_model()


class UserDetail(base_views.RetrieveUpdateAPIView):
    model = User
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_object(self, qs=None):
        obj = super().get_object()
        if not obj.is_active:
            raise exceptions.PermissionDenied()
        return obj


class UserList(base_views.ListAPIView):
    model = User
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)


class ActiveUserView(base_views.RetrieveAPIView):
    model = User
    serializer_class = serializers.ActiveUserSerializer
    view_name = 'Me'

    def get_object(self):
        try:
            obj = self.model.objects.get(pk=self.request.user.pk)
        except ObjectDoesNotExist:
            obj = AnonymousUser()
        return obj

