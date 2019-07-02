from django.db import models


class Ping(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
