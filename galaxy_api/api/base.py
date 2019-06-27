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

from django.core import exceptions as dj_exc
from django import http as dj_http

from django.shortcuts import get_object_or_404

from rest_framework import exceptions as drf_exc
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import status as http_codes
from rest_framework import views


def exception_handler(exc, context):
    if isinstance(exc, dj_http.Http404):
        data = {
            'code': drf_exc.NotFound.default_code,
            'message': drf_exc.NotFound.default_detail,
        }
        views.set_rollback()
        return Response(data, status=http_codes.HTTP_404_NOT_FOUND)

    if isinstance(exc, dj_exc.PermissionDenied):
        data = {
            'code': drf_exc.PermissionDenied.default_code,
            'message': drf_exc.PermissionDenied.default_detail,
        }
        views.set_rollback()
        return Response(data, status=http_codes.HTTP_403_FORBIDDEN)

    if isinstance(exc, drf_exc.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        data = {
            'code': exc.default_code,
            'message': exc.default_detail,
        }
        errors = []

        if isinstance(exc.detail, list):
            errors = [{'code': e.code, 'message': e} for e in exc.detail]
        elif isinstance(exc.detail, dict):
            for field, messages in exc.detail.items():
                if isinstance(messages, str):
                    messages = [messages]
                for message in messages:
                    error = {'code': message.code, 'message': message}
                    if field != api_settings.NON_FIELD_ERRORS_KEY:
                        error['field'] = field
                    errors.append(error)
        else:
            data['code'] = exc.detail.code
            data['message'] = exc.detail

        if len(errors) == 1 and 'field' not in errors[0]:
            data.update(errors[0])
        elif errors:
            data['errors'] = errors

        views.set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None


class ExceptionHandlerMixin:

    def get_exception_handler(self):
        return exception_handler


class APIView(ExceptionHandlerMixin,
              views.APIView):
    """Base class for API views."""
    pass


class GenericAPIView(APIView,
                     generics.GenericAPIView):
    """Base class for generic API views."""
    pass


class CreateAPIView(mixins.CreateModelMixin,
                    GenericAPIView):
    """
    Concrete view for creating a model instance.
    """
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAPIView(mixins.ListModelMixin,
                  GenericAPIView):
    """
    Concrete view for listing a queryset.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveAPIView(mixins.RetrieveModelMixin,
                      GenericAPIView):
    """
    Concrete view for retrieving a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DestroyAPIView(mixins.DestroyModelMixin,
                     GenericAPIView):
    """
    Concrete view for deleting a model instance.
    """
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateAPIView(mixins.UpdateModelMixin,
                    GenericAPIView):
    """
    Concrete view for updating a model instance.
    """
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SubListAPIView(ListAPIView):
    """Base class for a read-only sublist view.

    Subclasses should define at least:
      model = ModelClass
      serializer_class = SerializerClass
      parent_model = ModelClass
      relationship = 'rel_name_from_parent_to_model'
    And optionally (user must have given access permission on parent object
    to view sublist):
      parent_access = 'read'
    """

    def get_description_context(self):
        d = super().get_description_context()
        d.update({
            'parent_model_verbose_name':
                str(self.parent_model._meta.verbose_name),
            'parent_model_verbose_name_plural':
                str(self.parent_model._meta.verbose_name_plural),
        })
        return d

    def get_parent_object(self):
        parent_filter = {
            self.lookup_field: self.kwargs.get(self.lookup_field, None),
        }
        return get_object_or_404(self.parent_model, **parent_filter)

    def check_parent_access(self, parent=None):
        parent = parent or self.get_parent_object()

        # FIXME:
        return True

        # parent_access = getattr(self, 'parent_access', 'read')
        # if parent_access in ('read', 'delete'):
        #     args = (parent_access, parent)
        # else:
        #     args = (parent_access, parent, None)

        # FIXME:
        # if notcheck_user_access(self.request.user, self.parent_model, *args):
        #     # logger.debug('check_parent_access: parent_access=%s parent=%s',
        #     # parent_access, parent.__class__.__name__)
        #     raise PermissionDenied()

    def get_queryset(self):
        parent = self.get_parent_object()
        self.check_parent_access(parent)
        qs = self.model.objects.all().distinct()
        sublist_qs = getattr(parent, self.relationship).distinct()
        return qs & sublist_qs


class RetrieveUpdateAPIView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            GenericAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveDestroyAPIView(mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             GenericAPIView):
    """
    Concrete view for retrieving or deleting a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
