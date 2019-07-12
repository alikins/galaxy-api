from django.contrib import admin
from galaxy_api.auth import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass