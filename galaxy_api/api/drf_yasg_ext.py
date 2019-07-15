from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.inspectors import PaginatorInspector

from galaxy_api.api.pagination import InsightsStylePagination, PageNumberPagination


class PageNumberPaginationInspector(PaginatorInspector):
    """
    Provides the response schema to match the output of
    CustomPageNumberPagination as per IPP-12.
    """
    def get_paginated_response(self, paginator, response_schema):
        if not isinstance(paginator, PageNumberPagination):
            return super(PaginatorInspector,
                         self).get_paginated_response(paginator,
                                                      response_schema)

        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict((
                ('previous', openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                    x_nullable=True
                )),
                ('next', openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                    x_nullable=True
                )),
                (('results', response_schema)),
            )),
            required=['results'],
        )


class IPP12RestResponsePagination(PaginatorInspector):
    """
    Provides the response schema to match the output of
    CustomPageNumberPagination as per IPP-12.
    """
    def get_paginated_response(self, paginator, response_schema):
        if not isinstance(paginator, InsightsStylePagination):
            return super(PaginatorInspector, self).get_paginated_response(paginator, response_schema)

        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict((
                ('meta', openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=OrderedDict((
                        ('count', openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                        )),
                    )),
                    required=['count'],
                )),
                ('links', openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=OrderedDict((
                        ('first', openapi.Schema(
                            type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                            x_nullable=True
                        )),
                        ('previous', openapi.Schema(
                            type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                            x_nullable=True
                        )),
                        ('next', openapi.Schema(
                            type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                            x_nullable=True
                        )),
                        ('last', openapi.Schema(
                            type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                            x_nullable=True
                        )),
                    )),
                )),
                ('data', response_schema),
            )),
            required=['data'],
        )
