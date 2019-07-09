import logging

from collections import OrderedDict

# from allauth.account.models import EmailAddress

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from rest_framework import serializers

from . import base_serializer

logger = logging.getLogger(__name__)

User = get_user_model()

# USER_FIELDS = (
#     'id', 'url', 'related', 'summary_fields', 'created', 'modified',
#     'username', 'staff', 'full_name', 'date_joined', 'avatar_url'
# )
USER_FIELDS = (
    'id',
    'username', 'staff', 'date_joined',
)

__all__ = [
    'ActiveUserSerializer',
    'UserSerializer',
]


class ActiveUserSerializer(base_serializer.BaseSerializer):
    authenticated = serializers.SerializerMethodField()
    staff = serializers.ReadOnlyField(source='is_staff')
    primary_email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = USER_FIELDS + ('authenticated', 'primary_email')

    def get_summary_fields(self, obj):
        if not obj or not obj.is_authenticated:
            return {}
        d = super().get_summary_fields(obj)
        return d

    def get_authenticated(self, obj):
        return bool(obj.is_authenticated)

    def get_primary_email(self, obj):
        # if obj and not isinstance(obj, AnonymousUser):
        #     emails = EmailAddress.objects.filter(user=obj, primary=True)
        #     if emails:
        #         return emails[0].email
        return None


class UserSerializer(base_serializer.BaseSerializer):
    staff = serializers.ReadOnlyField(source='is_staff')

    class Meta:
        model = User
        fields = USER_FIELDS

    def get_related(self, obj):
        if not obj or not obj.is_authenticated:
            return {}
        res = super().get_related(obj)
        res.update(dict(
        ))
        return res

    def get_summary_fields(self, obj):
        if not obj or not obj.is_authenticated:
            return {}
        d = super().get_summary_fields(obj)
        # d['subscriptions'] = [
        #     OrderedDict([
        #         ('id', g.id),
        #         ('github_user', g.github_user),
        #         ('github_repo', g.github_repo)
        #     ]) for g in obj.subscriptions.all()]
        # d['starred'] = [
        #     OrderedDict([
        #         ('id', g.id),
        #         ('github_user', g.repository.github_user),
        #         ('github_repo', g.repository.github_repo)
        #     ]) for g in obj.starred.select_related('repository').all()]
        return d
