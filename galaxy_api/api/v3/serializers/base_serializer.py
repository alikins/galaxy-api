from collections import OrderedDict

from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rest_framework import serializers

SUMMARIZABLE_FK_FIELDS = {
    # 'owner': ('id', 'url', 'username', 'full_name', 'avatar_url'),
    'owner': ('id', 'username',),
}

BASE_FIELDS = ('id',
               'created', 'modified',)

User = get_user_model()


class BaseSerializer(serializers.ModelSerializer):

    # make certain fields read only
    created = serializers.SerializerMethodField()
    modified = serializers.SerializerMethodField()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.fields += ('created', 'modified', )

    def get_fields(self):
        # opts = get_concrete_model(self.Meta.model)._meta
        opts = self.Meta.model._meta.concrete_model._meta
        ret = super().get_fields()
        for key, field in ret.items():
            if key == 'id' and not getattr(field, 'help_text', None):
                field.help_text = u'Database ID for this {}.'.format(
                    opts.verbose_name)
            elif key == 'created':
                field.help_text = (
                    u'Timestamp when this {} was created.'.format(
                        opts.verbose_name))
                field.type_label = 'datetime'
            elif key == 'modified':
                field.help_text = (
                    u'Timestamp when this {} was last modified.'.format(
                        opts.verbose_name))
                field.type_label = 'datetime'
        return ret

    def get_created(self, obj):
        if obj is None:
            return None
        elif isinstance(obj, User):
            return obj.date_joined
        else:
            try:
                return obj.created
            except AttributeError:
                return None

    def get_modified(self, obj):
        if obj is None:
            return None
        elif isinstance(obj, User):
            return obj.last_login  # Not actually exposed for User.
        else:
            try:
                return obj.modified
            except AttributeError:
                return None