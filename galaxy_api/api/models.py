from django.db import models

from galaxy_api import constants as const
from galaxy_api.auth import models as auth_models


__all__ = (
    'Namespace'
)


class Namespace(models.Model):
    """
    A model representing Ansible content namespace.

    :var name: Namespace name. Must be lower case containing
        only alphanumeric characters and underscores.
    :var owners: Reference to a namespace owners.

    """

    # Fields
    name = models.CharField(max_length=const.MAX_NAME_LENGTH, unique=True, editable=False)

    # References
    owners = models.ManyToManyField(auth_models.User)


class Collection(models.Model):
    """
    A model representing Ansible content collection.

    :var name: Collection name. Must be lower case containing
        only alphanumeric characters and underscores.
    :var remote_id: Collection ID in remote database.
    :var namespace: Reference to a collection namespace
    """

    # Fields
    name = models.CharField(max_length=const.MAX_NAME_LENGTH, editable=False)
    remote_id = models.UUIDField(unique=True, editable=False)

    quality_score = models.FloatField(null=True, editable=False)

    # References
    namespace = models.ForeignKey(Namespace, on_delete=models.CASCADE, editable=False)

    class Meta:
        unique_together = (
            'namespace',
            'name',
        )
