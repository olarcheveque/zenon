# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0002_auto_20160123_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='permission',
            field=models.CharField(max_length=100, choices=[('permissions.journal:can_manage', '[Revue] Peut gérer les revues'), ('all:can_manage_issuesubmission', '[Utilisateur] Peut gérer le dépôt de fichier')]),
        ),
    ]
