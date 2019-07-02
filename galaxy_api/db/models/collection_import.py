import logging

import attr

from django.db import models
from django.contrib.postgres import fields as psql_fields

from galaxy.importer.utils import lint as lintutils

from .collection import CollectionVersion
from .namespace import Namespace
from .task import Task


class CollectionImport(Task):
    """Collection import task info."""

    name = models.CharField(max_length=64)
    version = models.CharField(max_length=64)

    messages = psql_fields.JSONField(default=list)
    lint_records = psql_fields.JSONField(default=list)

    namespace = models.ForeignKey(Namespace, on_delete=models.CASCADE)
    imported_version = models.ForeignKey(
        CollectionVersion, null=True, on_delete=models.SET_NULL,
        related_name='import_tasks')

    def add_log_record(self, record: logging.LogRecord):
        self.messages.append({
            'message': record.msg,
            'level': record.levelname,
            'time': record.created,
        })

    def add_lint_record(self, lint_record: lintutils.LintRecord) -> None:
        self.lint_records.append(attr.asdict(lint_record))

    def get_message_stats(self):
        """Returns total number of errors and warnings."""
        # TODO(cutwater): Replace with SQL query
        errors, warnings = 0, 0
        for msg in self.messages:
            if msg['level'] == 'ERROR':
                errors += 1
            elif msg['level'] == 'WARNING':
                warnings += 1
        return errors, warnings
