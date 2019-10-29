import mimetypes

from rest_framework import serializers

from galaxy_api.api.utils import parse_collection_filename


class CollectionUpdateSerializer(serializers.Serializer):
    """A serializer for a Collection update."""

    deprecated = serializers.BooleanField(required=False)
    namespace = serializers.CharField(required=True)
    name = serializers.CharField(required=True)


class CollectionUploadSerializer(serializers.Serializer):
    """
    A serializer for the Collection One Shot Upload API.
    """

    file = serializers.FileField(required=True)

    sha256 = serializers.CharField(required=False, default=None)

    def to_internal_value(self, data):
        """Parse and validate collection filename."""
        data = super().to_internal_value(data)

        filename = data["file"].name
        data.update({
            "filename": parse_collection_filename(filename),
            "mimetype": (mimetypes.guess_type(filename)[0] or 'application/octet-stream')
        })
        return data
