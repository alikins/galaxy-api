from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from galaxy_api.api import models as api_models


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content_type', 'codename')
    raw_id_fields = ('content_type',)
    search_fields = ('name', 'content_type__app_label', 'content_type__model', 'codename')


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'app_label', 'model')


@admin.register(api_models.Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'description')
    fields = ('name', 'company', 'email', 'avatar_url', 'description', 'groups')
    autocomplete_fields = ['groups']
    search_fields = ['groups__name', 'name', 'company', 'email']


@admin.register(api_models.NamespaceLink)
class NamespaceLinkAdmin(admin.ModelAdmin):
    list_display = ('namespace', 'name', 'url')
    fields = ('name', 'url', 'namespace')
    search_fields = ['namespace__name', 'namespace__company', 'name', 'url']


@admin.register(api_models.CollectionImport)
class CollectionImportAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'created_at', 'namespace', 'name', 'version')
    fields = ('task_id', 'created_at', 'namespace', 'name', 'version')
    readonly_fields = ('name', 'version')
    date_hierarchy = 'created_at'
    search_fields = ['namespace__name', 'namespace__company', 'name']
    view_on_site = True
