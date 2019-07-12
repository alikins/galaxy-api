from django.contrib import admin
from galaxy_api.api import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'name', )
    list_display = ('name','id')
    search_fields = ('id', 'name', )


@admin.register(models.Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    autocomplete_fields = ('owners', )
    readonly_fields = ('name',)
    fields = ('name', 'owners')


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    readonly_fields = ('namespace', 'name', 'remote_id',)
    list_display = ('__str__', 'namespace', 'name', 'remote_id')
    search_fields = ('namespace__name', 'name', 'remote_id')
