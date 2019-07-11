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

from django.contrib.postgres import indexes as psql_indexes
from django.contrib.postgres import fields as psql_fields
from django.contrib.postgres import search as psql_search
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models

from galaxy_api import constants as const
from . import mixins


class Collection(mixins.TimestampsMixin, models.Model):
    """
    A model representing an Ansible Content Collection.

    :var name: Collection name. Must be lower case containing
        only alphanumeric characters and underscores.
    :var remote_id: Collection ID in remote database.
    :var namespace: Reference to a collection namespace
    :var tags: List of a last collection version tags.
    """
    # Fields
    name = models.CharField(max_length=const.MAX_NAME_LENGTH, editable=False)
    remote_id = models.UUIDField(unique=True, editable=False)

    quality_score = models.FloatField(null=True, editable=False)

    # References
    namespace = models.ForeignKey(Namespace, on_delete=models.CASCADE, editable=False)

    tags = models.ManyToManyField('Tag')

    class Meta:
        unique_together = (
            'namespace',
            'name',
        )

    def __str__(self):
        return '{}.{}'.format(self.namespace, self.name)


class CollectionVersion(mixins.TimestampsMixin):
    """
    A model representing an Ansible Content Collection version.

    :var version: Collection version string in semantic version format.
    :var hidden: Indicates if a version should not be displayed and allowed
        for installation.
    :var metadata: Collection metadata in JSON format.
    :var contents: Collection contents in JSON format.
    :var collection: A reference to a related collection object.
    """

    TYPE = 'collection-version'

    # in theory, pulp_ansible provides a url like
    # pulp_ansible/galaxy/(?P<path>.+)/api/v2/collections/(?P<namespace>[^/]+)/(?P<name>[^/]+)/'r'versions/(?P<version>[^/]
    # assuming that is enough to get the galaxy artifact details and download
    # the collection artifact

    # Fields
    version = models.CharField(max_length=64)
    hidden = models.BooleanField(default=False)

    metadata = psql_fields.JSONField(default=dict)
    contents = psql_fields.JSONField(default=list)
    quality_score = models.FloatField(
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )

    readme_mimetype = models.CharField(max_length=32, blank=True)
    readme_text = models.TextField(blank=True)
    readme_html = models.TextField(blank=True)

    # References
    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, related_name='versions')

    class Meta:
        unique_together = (
            'collection',
            'version',
        )

    def __str__(self):
        return '{}.{}-{}'.format(
            self.collection.namespace,
            self.collection.name,
            self.version
        )

    def get_content_artifact(self):
        """Returns whatever the pulp rest api equiv of a  ContentArtifact is

        object related to collection version."""

        return {}

    # need update
    def get_download_url(self) -> str:
        """Builds artifact download url pointing to Pulp's content app."""
        prefix = settings.GALAXY_DOWNLOAD_URL
        repository = settings.GALAXY_PULP_REPOSITORY
        ca = self.get_content_artifact()
        return '/' + '/'.join(
            s.strip('/') for s in (prefix, repository, ca.relative_path))
