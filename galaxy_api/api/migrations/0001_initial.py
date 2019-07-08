from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("galaxy_auth", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Namespace",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, unique=True, editable=False)),
                ("owners", models.ManyToManyField(to="galaxy_auth.User")),
            ],
        ),
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, editable=False)),
                ("remote_id", models.UUIDField(unique=True, editable=False)),
                ('quality_score', models.FloatField(null=True, editable=False)),
                (
                    "namespace",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        to="galaxy_api.Namespace",
                        editable=False
                    ),
                ),
            ],
            options={"unique_together": {("namespace", "name")}},
        ),
    ]
