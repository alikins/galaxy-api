from collections import OrderedDict

from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rest_framework import serializers

SUMMARIZABLE_FK_FIELDS = {
    'owner': ('id', 'url', 'username', 'full_name', 'avatar_url'),
    'role': ('id', 'url', 'name',),
}

BASE_FIELDS = ('id', 'url', 'related', 'summary_fields',
               'created', 'modified', 'name')

User = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    # add the URL and related resources
    url = serializers.SerializerMethodField()
    related = serializers.SerializerMethodField()
    summary_fields = serializers.SerializerMethodField()

    # make certain fields read only
    created = serializers.SerializerMethodField()
    modified = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.fields += ('url', 'related', 'summary_fields',
                             'created', 'modified', 'active')

    def get_fields(self):
        # opts = get_concrete_model(self.Meta.model)._meta
        opts = self.Meta.model._meta.concrete_model._meta
        ret = super().get_fields()
        for key, field in ret.items():
            if key == 'id' and not getattr(field, 'help_text', None):
                field.help_text = u'Database ID for this {}.'.format(
                    opts.verbose_name)
            elif key == 'url':
                field.help_text = u'URL for this {}.'.format(opts.verbose_name)
                field.type_label = 'string'
            elif key == 'related':
                field.help_text = (
                    'Data structure with URLs of related resources.')
                field.type_label = 'object'
            elif key == 'summary_fields':
                field.help_text = (
                    'Data structure with name/description '
                    'for related resources.')
                field.type_label = 'object'
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

    def get_url(self, obj):
        if obj is None or isinstance(obj, AnonymousUser):
            return ''
        elif isinstance(obj, User):
            return reverse('api:v1:user_detail', args=(obj.pk,))
        else:
            try:
                return obj.get_absolute_url()
            except AttributeError:
                return ''

    def get_related(self, obj):
        res = OrderedDict()
        if getattr(obj, 'owner', None):
            res['owner'] = reverse('api:v1:user_detail', args=(obj.owner.pk,))
        return res

    def get_summary_fields(self, obj):
        # Return values for certain fields on related objects, to simplify
        # displaying lists of items without additional API requests.
        summary_fields = dict()
        for fk, related_fields in SUMMARIZABLE_FK_FIELDS.items():
            try:
                fkval = getattr(obj, fk, None)
                if fkval is not None:
                    summary_fields[fk] = dict()
                    for field in related_fields:
                        fval = getattr(fkval, field, None)
                        if fval is not None:
                            summary_fields[fk][field] = fval
            # Can be raised by the reverse accessor for a OneToOneField.
            except ObjectDoesNotExist:
                pass
        return summary_fields

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

    def get_active(self, obj):
        if obj is None:
            return False
        elif isinstance(obj, User):
            return obj.is_active
        else:
            try:
                return obj.active
            except AttributeError:
                return None
