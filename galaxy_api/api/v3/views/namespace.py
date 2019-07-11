# (c) 2012-2018, Ansible by Red Hat
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

import logging
import re

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

# filter backends
from rest_framework.filters import SearchFilter
from galaxy_api.api.filters import FieldLookupBackend, OrderByBackend

from rest_framework import status
from rest_framework.exceptions import (
    ValidationError, APIException, PermissionDenied
)
from rest_framework.response import Response

from galaxy_api.api.v3 import serializers
from galaxy_api.api import models
from galaxy_api.api import base as base_views


__all__ = [
    'NamespaceList',
    'NamespaceDetail',
]

GalaxyUser = get_user_model()

logger = logging.getLogger(__name__)


def check_basic(data, errors, instance=None):
    name = data.get('name')

    # The database still contains legacy namesapces with invalid chars in them
    # This can cause errors when users with legacy names try to update other
    # information about their namespace (owners, description etc.) To fix this,
    # just skip checks if the name isn't being update and assume that whatever
    # is in the database is correct.
    if name and instance:
        if name == instance.name:
            return

    if not name:
        errors['name'] = "Attribute 'name' is required"
    elif not re.match(r'^[a-zA-Z0-9_]+$', name):
        # Allow only names containing word chars
        errors['name'] = "Name can only contain [A-Za-z0-9_]"
    elif(len(name) <= 2):
        errors['name'] = "Name must be longer than 2 characters"
    elif(name.startswith('_')):
        errors['name'] = "Name cannot begin with '_'"


def check_owners(data_owners):
    if not isinstance(data_owners, list):
        errors = 'Invalid type. Expected list'
        return errors, []

    owners = []
    errors = {}
    for i in range(0, len(data_owners)):
        owner = data_owners[i]
        if not isinstance(owner, dict):
            logger.debug('owner: %s', owner)
            errors[i] = 'Invalid type. Expected dictionary'
            continue
        if not owner.get('id'):
            errors[i] = "Attribute 'id' is required %s" % owner
            continue
        try:
            GalaxyUser.objects.get(pk=owner['id'])
        except ObjectDoesNotExist:
            errors[i] = "A user does not exist for this 'id'"
            continue
        if owner['id'] not in owners:
            owners.append(owner['id'])
    return errors, owners


def can_update(namespace_id, user_id):
    namespace = models.Namespace.objects.get(pk=namespace_id)
    if not namespace.owners.filter(pk=user_id):
        return False

    return True

def update_owners(instance, owners):
    for owner_pk in owners:
        # add new owners
        if not instance.owners.filter(pk=owner_pk):
            try:
                owner = GalaxyUser.objects.get(pk=owner_pk)
            except ObjectDoesNotExist:
                pass
            else:
                instance.owners.add(owner)

    for owner in [o for o in instance.owners.all() if o.pk not in owners]:
        # remove owners not in request owners
        instance.owners.remove(owner)


class NamespaceList(base_views.ListCreateAPIView):
    model = models.Namespace
    serializer_class = serializers.NamespaceSerializer
    queryset = models.Namespace.objects.all()
    # excludes ActiveOnly
    filter_backends = (FieldLookupBackend, SearchFilter, OrderByBackend)

    def post(self, request, *args, **kwargs):
        data = request.data
        errors = {}
        owners = []

        check_basic(data, errors)

        if data.get('name'):
            try:
                models.Namespace.objects.get(name__iexact=data['name'].lower())
                errors['name'] = "A namespace with this name already exists"
            except ObjectDoesNotExist:
                pass

        # FIXME
        if data.get('owners'):
            owner_errors, owners = check_owners(data['owners'])
            owner_errors = []
            if owner_errors:
                errors['owners'] = owner_errors

        if errors:
            raise ValidationError(detail=errors)

        # FIXME
        #if not request.user.is_staff and not can_update(
        #        data['id'], request.user.id):
        #    owners.append(request.user.id)

        sanitized_name = data['name'].lower().replace('-', '_')

        namespace_attributes = {
            'name': sanitized_name,
        }

        #for item in ():
        #    if item in data:
        #        namespace_attributes[item] = data[item]

        try:
            namespace = models.Namespace.objects.create(**namespace_attributes)
        except Exception as exc:
            raise APIException(
                'Error creating namespace: {0}'.format(exc)
            )

        # FIXME
        update_owners(namespace, owners)

        serializer = self.get_serializer(instance=namespace)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NamespaceDetail(base_views.RetrieveUpdateDestroyAPIView):
    model = models.Namespace
    serializer_class = serializers.NamespaceSerializer
    queryset = models.Namespace.objects.all()

    # excludes ActiveOnly
    filter_backends = (FieldLookupBackend, SearchFilter, OrderByBackend)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        errors = {}
        owners = []

        # if no name is submitted on the form, it won't get updated so we can
        # ignore the name check
        if data.get('name') is not None:
            check_basic(data, errors, instance=instance)

        # FIXME
        # if data.get('owners'):
        #     owner_errors, owners = check_owners(data['owners'])
        #     if owner_errors:
        #         errors['owners'] = owner_errors

        if errors:
            raise ValidationError(detail=errors)

        if not request.user.is_staff and not can_update(
                data['id'], request.user.id):
            raise PermissionDenied(
                "User does not have access to "
                "Namespace {0}".format(data.get('name', ''))
            )

        # FIXME
        # if data.get('owners'):
        #     update_owners(instance, owners)

        to_update = []

        if request.user.is_staff:
            to_update.append('name')

        for item in to_update:
            if item in data:
                setattr(instance, item, data[item])
        instance.save()

        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
