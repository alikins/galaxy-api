
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

from django.urls import reverse

from .base import (
    CommonModel,
)


class Tag(CommonModel):
    """A class representing the tags that have been assigned to roles."""

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('api:v3:tag_detail', args=(self.pk,))

    def get_num_roles(self):
        return self.roles.filter(active=True, is_valid=True).count()
