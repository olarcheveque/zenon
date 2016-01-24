# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rule',
            options={'verbose_name': 'Règle'},
        ),
        migrations.AlterField(
            model_name='rule',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', blank=True, null=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='rule',
            name='object_id',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='permission',
            field=models.CharField(choices=[('permissions.journal:can_access', '[Revue] Peut accéder'), ('permissions.journal:can_upload_issuesubmission', '[Revue] Peut déposer un numéro'), ('permissions.policy:can_access', '[Accès] Peut accéder'), ('permissions.policy:can_change', '[Accès] Peut modifier')], max_length=100),
        ),
    ]
