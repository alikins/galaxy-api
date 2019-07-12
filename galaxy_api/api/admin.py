from django.contrib import admin
from galaxy_api.api import models



@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass
    # search_fields = ('name', )


@admin.register(models.Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    pass
    # autocomplete_fields = ('owners', )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass
    # autocomplete_fields = ('tags', )
    # readonly_fields = ('latest_version', )
