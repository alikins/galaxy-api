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

from rest_framework import pagination
from rest_framework import response
from rest_framework.utils.urls import replace_query_param

log = logging.getLogger(__name__)

# TODO/FIXME(AKL) - pull from env
API_VERSION = 'v3' 


# From https://github.com/RedHatInsights/insights-advisor-api/blob/master/advisor/api/utils.py
class InsightsStylePagination(pagination.LimitOffsetPagination):
    """Create standard paginiation class with page size."""

    default_limit = 10
    max_limit = 1000

    @staticmethod
    def link_rewrite(request, link):
        """Rewrite the link based on the path header to only provide partial url."""
        url = link
        version = 'v{}/'.format(API_VERSION)
        if 'PATH_INFO' in request.META:
            try:
                local_api_index = link.index(version)
                path = request.META.get('PATH_INFO')
                path_api_index = path.index(version)
                path_link = '{}{}'
                url = path_link.format(path[:path_api_index],
                                       link[local_api_index:])
            except ValueError:
                log.warning('Unable to rewrite link as "{}" was not found.'.format(version))
        return url

    def get_first_link(self):
        """Create first link with partial url rewrite."""
        url = self.request.build_absolute_uri()
        offset = 0
        first_link = replace_query_param(url, self.offset_query_param, offset)
        first_link = replace_query_param(first_link, self.limit_query_param, self.limit)
        return InsightsStylePagination.link_rewrite(self.request, first_link)

    def get_next_link(self):
        """Create next link with partial url rewrite."""
        next_link = super().get_next_link()
        if next_link is None:
            return self.get_last_link()
        return InsightsStylePagination.link_rewrite(self.request, next_link)

    def get_previous_link(self):
        """Create previous link with partial url rewrite."""
        previous_link = super().get_previous_link()
        if previous_link is None:
            return self.get_first_link()
        return InsightsStylePagination.link_rewrite(self.request, previous_link)

    def get_last_link(self):
        """Create last link with partial url rewrite."""
        url = self.request.build_absolute_uri()
        offset = self.count - self.limit if (self.count - self.limit) >= 0 else 0
        last_link = replace_query_param(url, self.offset_query_param, offset)
        last_link = replace_query_param(last_link, self.limit_query_param, self.limit)
        return InsightsStylePagination.link_rewrite(self.request, last_link)

    def get_paginated_response(self, data):
        """Override pagination output."""
        return response.Response({
            'meta': {
                'count': self.count,
            },
            'links': {
                'first': self.get_first_link(),
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'last': self.get_last_link()
            },
            'data': data
        })
