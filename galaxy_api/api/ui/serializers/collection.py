from rest_framework import serializers

from .namespace import NamespaceSerializer

import logging
import pprint
log = logging.getLogger(__name__)

class ContentSummarySerializer(serializers.Serializer):

    def to_representation(self, contents):
        summary = {"role": [], "module": [], "playbook": [], "plugin": []}
        for item in contents:
            key = self._get_content_type_key(item["content_type"])
            summary[key].append(item['name'])
        return {"total_count": sum(map(len, summary.items())), "contents": summary}

    @staticmethod
    def _get_content_type_key(content_type: str) -> str:
        # FIXME(cutwater): Replace with galaxy-importer constants usage
        if content_type == "role":  # ContentType.ROLE (from galaxy-importer)
            return "role"
        elif content_type == "module":  # ContentType.MODULE (from galaxy-importer)
            return "module"
        elif content_type == "playbook":  # ContentType.PLAYBOOK (from galaxy-importer)
            return "playbook"
        else:
            return "plugin"

class ContentSerializer(serializers.Serializer):
    name = serializers.CharField()
    content_type = serializers.CharField()
    description = serializers.CharField()

class CollectionVersionSummarySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    version = serializers.CharField()
    created = serializers.CharField()

class CollectionMetadataBaseSerializer(serializers.Serializer):
    description = serializers.CharField()
    authors = serializers.ListField(serializers.CharField())
    license = serializers.ListField(serializers.CharField())
    tags = serializers.SerializerMethodField()

    def get_tags(self, metadata):
        return [tag['name'] for tag in metadata['tags']]


class CollectionMetadataSerializer(CollectionMetadataBaseSerializer):
    dependencies = serializers.JSONField()
    contents = serializers.JSONField()

    # URLs
    documentation = serializers.CharField()
    homepage = serializers.CharField()
    issues = serializers.CharField()
    repository = serializers.CharField()


class CollectionVersionBaseSerializer(serializers.Serializer):
    namespace = serializers.CharField()
    name = serializers.CharField()
    version = serializers.CharField()
    docs_blob = serializers.JSONField()
    # content_summary = ContentSummarySerializer(source='contents')
    created_at = serializers.DateTimeField(source='_created')

    contents = serializers.ListField(ContentSerializer())


class CollectionLatestVersionSerializer(CollectionVersionBaseSerializer):
    metadata = CollectionMetadataBaseSerializer(source='*')


class CollectionVersionSerializer(CollectionMetadataBaseSerializer):
    metadata = CollectionMetadataSerializer(source="*")
    docs_blob = serializers.JSONField()


class _CollectionSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    namespace = serializers.SerializerMethodField()
    name = serializers.CharField()
    download_count = serializers.IntegerField(default=0)

    latest_version = CollectionLatestVersionSerializer(source='*')
    # all_versions = serializers.ListField(CollectionVersionSummarySerializer())
    all_versions = serializers.SerializerMethodField()
    # all_versions = serializers.ListField(child=serializers.DictField())
    # content_summary = ContentSummarySerializer(source='contents')

    def _get_namespace(self, obj):
        raise NotImplementedError

    def get_namespace(self, obj):
        log.debug('obj: %s', pprint.pformat(obj))
        namespace = self._get_namespace(obj)
        return NamespaceSerializer(namespace).data

    def _get_all_versions(self, obj):
        #log.debug('obj: %s', pprint.pformat(obj))
        log.debug('self.context: %s', pprint.pformat(self.context))
        return self.context['all_versions']

    def get_all_versions(self, obj):
        all_versions_data = self._get_all_versions(obj)
        return [CollectionVersionSummarySerializer(version).data for version in all_versions_data]
        # return serializers.ListField(child=CollectionVersionSummarySerializer())

class CollectionListSerializer(_CollectionSerializer):
    def _get_namespace(self, obj):
        name = obj['namespace']
        return self.context['namespaces'].get(name, None)


class CollectionDetailSerializer(_CollectionSerializer):

    def _get_namespace(self, obj):
        return self.context['namespace']
