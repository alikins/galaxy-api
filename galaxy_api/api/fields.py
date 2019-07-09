
# (c) 2012-2019, Ansible by Red Hat
#
# This file is part of Ansible Galaxy
#
# Ansible Galaxy is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by
# the Apache Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Ansible Galaxy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Apache License for more details.
#
# You should have received a copy of the Apache License
# along with Galaxy.  If not, see <http://www.apache.org/licenses/>.

import datetime as dt
import distutils.version

from django.db import models

from rest_framework import serializers
from rest_framework.reverse import reverse

import semantic_version


class NativeTimestampField(serializers.DateTimeField):
    """Represents internal timestamp value as date time string."""

    def to_representation(self, value):
        if value is None:
            return None

        value = dt.datetime.utcfromtimestamp(value).replace(
            tzinfo=dt.timezone.utc)
        return super().to_representation(value)

    def to_internal_value(self, value):
        if value is None:
            return None
        value = super().to_internal_value(value)
        return value.astimezone(dt.timezone.utc).timestamp()


class NamespaceObjectField(serializers.Field):
    """Return namespace object for a serializer field."""
    def to_representation(self, value):
        return {
            'id': value.pk,
            'href': reverse(
                'api:namespace_detail',
                kwargs={'pk': value.pk},
                request=self.context.get('request'),
            ),
            'name': value.name,
        }


class VersionUrlField(serializers.Field):
    """Return version detail url under collection namespace and name."""
    def to_representation(self, value):
        return reverse(
            'api:v2:version-detail',
            kwargs={
                'namespace': value.collection.namespace.name,
                'name': value.collection.name,
                'version': value.version,
            },
            request=self.context.get('request'),
        )


class VersionField(models.CharField):
    """Semantic version field"""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 64)
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return semantic_version.Version(value)

    def to_python(self, value):
        if isinstance(value, semantic_version.Version):
            return value
        if value is None:
            return value
        return semantic_version.Version(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return str(value)


# TODO(cutwater): LooseVersionField is not used in actual models and is kept
# only because it's referenced by migration 0001_initial.py
class LooseVersionField(models.Field):
    """ store and return values as a LooseVersion """

    def db_type(self, connection):
        return 'varchar(64)'

    def get_internal_type(self):
        return 'CharField'

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def to_python(self, value):
        return distutils.version.LooseVersion(value)

    def get_prep_value(self, value):
        return str(value)


# From: http://stackoverflow.com/questions/3459843/auto-truncating-fields-at-max-length-in-django-charfields # noqa: E501
class TruncatingCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value and len(value) > self.max_length:
            return value[:self.max_length - 3] + '...'
        return value
