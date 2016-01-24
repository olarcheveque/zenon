# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('erudit', '0015_journal_localidentifier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date_creation', models.DateTimeField(default=django.utils.timezone.now, editable=False, null=True, verbose_name='Date de création')),
                ('date_modification', models.DateTimeField(default=django.utils.timezone.now, editable=False, null=True, verbose_name='Date de modification')),
                ('object_id', models.PositiveIntegerField()),
                ('permission', models.CharField(choices=[('can_upload_issuesubmission', 'Peut déposer un numéro')], max_length=100)),
                ('content_type', models.ForeignKey(verbose_name='Type', to='contenttypes.ContentType')),
                ('group', models.ForeignKey(blank=True, to='auth.Group', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Permission',
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
            ],
            options={
                'verbose_name': 'Revue',
                'proxy': True,
            },
            bases=('erudit.journal',),
        ),
    ]
