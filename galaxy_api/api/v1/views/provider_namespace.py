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

from django.core.exceptions import ObjectDoesNotExist

# filter backends
from rest_framework.filters import SearchFilter
from galaxy_api.api.filters import FieldLookupBackend, OrderByBackend

from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response

from galaxy_api import models

# from galaxy_api.api import serializers
from galaxy_api.api.v1 import serializers
from galaxy_api.api import base as base_views
# from ..githubapi import GithubAPI

__all__ = [
    'ProviderNamespaceList',
    'ProviderNamespaceDetail',
    # 'ProviderNamespaceRepositoriesList'
]

log = logging.getLogger(__name__)


def check_provider_access(provider, user, name):
    if provider.name.lower() == 'github':


        # FIXME: plugin in rhsso namespace provider
        # user_namespaces = GithubAPI(user=user).user_namespaces()
        user_namespaces = [{'name': name}]  # Everyone gets a free namespace!


        match = False
        for ns in user_namespaces:
            if ns['name'] == name:
                match = True
                break
        if not match:
            raise APIException(
                "User does not have access to namespace "
                "{0} in GitHub".format(name)
            )


def check_namespace_access(user, namespace_id):

    # log.warning('NOT ACTUALLY CHECKING NAMESPACE ACCESS FOR user=%s namespace_id=%s', user, namespace_id)
    # return namespace_id
    log.debug('user=%r', user)
    log.debug('namespace_id=%s', namespace_id)

    try:
        namespace = user.namespaces.get(pk=namespace_id, active=True)
    except ObjectDoesNotExist:
        raise APIException("You do not have access to the requested namespace")
    return namespace


class ProviderNamespaceList(base_views.ListCreateAPIView):
    model = models.ProviderNamespace
    serializer_class = serializers.ProviderNamespaceSerializer
    queryset = models.ProviderNamespace.objects.all()
    # excludes ActiveOnly
    filter_backends = (FieldLookupBackend, SearchFilter, OrderByBackend)

    # def get_queryset(self):
    #     if getattr(self, 'swagger_fake_view', False):
    #         return []


    #     # FIXME:
    #     return models.ProviderNamespace.objects.all()


    #     # return super(ProviderNamespaceList, self).get_queryset()

    def post(self, request, *args, **kwargs):
        data = request.data

        if not data.get('name'):
            raise ValidationError(detail={"name": "a value is required"})

        if not data.get('namespace'):
            raise ValidationError(detail={"namespace": "a value is required"})

        if not data.get('provider'):
            raise ValidationError(detail={"provider": "a value is required"})

        # FIXME:
        try:
            namespace = check_namespace_access(request.user, data['namespace'])
        except APIException:
            raise

        try:
            provider = models.Provider.objects.get(pk=data['provider'])
        except ObjectDoesNotExist:
            raise ValidationError(
                detail={'provider': 'provider does not exist'}
            )

        try:
            models.ProviderNamespace.objects.get(
                name=data['name'], provider=provider
            )
        except ObjectDoesNotExist:
            pass
        else:
            raise APIException(
                "The requested provider namespace already exists"
            )

        try:
            check_provider_access(provider, request.user, data['name'])
        except APIException:
            raise

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data['provider'] = provider
        data['namespace'] = namespace
        obj = models.ProviderNamespace.objects.create(**data)
        serializer = self.get_serializer(obj)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class ProviderNamespaceDetail(base_views.RetrieveUpdateDestroyAPIView):
    model = models.ProviderNamespace
    serializer_class = serializers.ProviderNamespaceSerializer
    queryset = models.ProviderNamespace.objects.all()
    # excludes ActiveOnly
    filter_backends = (FieldLookupBackend, SearchFilter, OrderByBackend)

    # def get_queryset(self):
    #     if getattr(self, 'swagger_fake_view', False):
    #         return []
    #     return super(ProviderNamespaceDetail, self).get_queryset()

    def update(self, request, *args, **kwargs):
        data = request.data
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        try:
            check_namespace_access(request.user, instance.namespace.pk)
        except APIException:
            raise

        if data.get('namespace'):
            # User attempting to change the namespace
            try:
                namespace = models.Namespace.objects.get(
                    pk=data['namespace'], active=True
                )
            except ObjectDoesNotExist:
                raise ValidationError(
                    detail={'namespace': 'namespace does not exist'}
                )
            try:
                request.user.namespaces.get(pk=namespace.pk, active=True)
            except ObjectDoesNotExist:
                raise ValidationError(
                    detail={
                        'namespace': 'you do not have access to this namespace resource'
                    }
                )
            data['namespace'] = namespace

        if data.get('provider'):
            try:
                provider = models.Provider.objects.get(pk=data['provider'])
            except ObjectDoesNotExist:
                raise ValidationError(
                    detail={'provider': 'provider does not exist'}
                )
        else:
            provider = instance.provider

        try:
            check_provider_access(provider, request.user, data['name'])
        except APIException:
            raise

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        models.ProviderNamespace.objects.filter(pk=instance.pk).update(**data)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            check_namespace_access(request.user, instance.namespace.pk)
        except APIException:
            raise
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ProviderNamespaceRepositoriesList(base_views.SubListAPIView):
#     view_name = "Provider Namespace Repositories"
#     model = models.Repository
#     serializer_class = serializers.RepositorySerializer
#     parent_model = models.ProviderNamespace
#     relationship = "repositories"
