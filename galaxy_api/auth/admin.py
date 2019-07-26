from django.contrib import admin
from galaxy_api.auth import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__',
                    'id',
                    'username',
                    'first_name',
                    'last_name',
                    'email')

    list_filter = ('is_superuser',
                   'is_staff')

    search_fields = ('username',
                     'first_name',
                     'last_name',
                     'email')
