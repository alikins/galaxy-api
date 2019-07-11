# Generated by Django 2.2.3 on 2019-07-11 13:51

import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import galaxy_api.api.fields
import galaxy_api.api.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', galaxy_api.api.fields.TruncatingCharField(blank=True, default='', max_length=255)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('name', models.CharField(db_index=True, max_length=512, unique=True)),
                ('download_url', models.CharField(max_length=256, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model, galaxy_api.api.models.mixins.DirtyMixin),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', galaxy_api.api.fields.TruncatingCharField(blank=True, default='', max_length=255)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('name', models.CharField(db_index=True, max_length=512, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'ordering': ['name'],
            },
            bases=(models.Model, galaxy_api.api.models.mixins.DirtyMixin),
        ),
        migrations.AlterModelOptions(
            name='namespace',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='collection',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collection',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='namespace',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='namespace',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='namespace',
            name='owners',
            field=models.ManyToManyField(related_name='namespaces', to='galaxy_auth.User'),
        ),
        migrations.AddField(
            model_name='collection',
            name='tags',
            field=models.ManyToManyField(to='galaxy_api.Tag'),
        ),
        migrations.CreateModel(
            name='ProviderNamespace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', galaxy_api.api.fields.TruncatingCharField(blank=True, default='', max_length=255)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('display_name', models.CharField(blank=True, editable=False, max_length=256, null=True, verbose_name='Display Name')),
                ('avatar_url', models.CharField(blank=True, max_length=256, null=True, verbose_name='Avatar URL')),
                ('location', models.CharField(blank=True, max_length=256, null=True, verbose_name='Location')),
                ('company', models.CharField(blank=True, max_length=256, null=True, verbose_name='Company Name')),
                ('email', models.CharField(blank=True, max_length=256, null=True, verbose_name='Email Address')),
                ('html_url', models.CharField(blank=True, max_length=256, null=True, verbose_name='Web Site URL')),
                ('followers', models.IntegerField(null=True, verbose_name='Followers')),
                ('namespace', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provider_namespaces', to='galaxy_api.Namespace', verbose_name='Namespace')),
                ('provider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provider_namespaces', to='galaxy_api.Provider', verbose_name='Provider')),
            ],
            options={
                'ordering': ('provider', 'name'),
                'unique_together': {('provider', 'name'), ('namespace', 'provider', 'name')},
            },
            bases=(models.Model, galaxy_api.api.models.mixins.DirtyMixin),
        ),
        migrations.CreateModel(
            name='CollectionVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('version', models.CharField(max_length=64)),
                ('hidden', models.BooleanField(default=False)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('contents', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('quality_score', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('readme_mimetype', models.CharField(blank=True, max_length=32)),
                ('readme_text', models.TextField(blank=True)),
                ('readme_html', models.TextField(blank=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='galaxy_api.Collection')),
            ],
            options={
                'unique_together': {('collection', 'version')},
            },
        ),
    ]
