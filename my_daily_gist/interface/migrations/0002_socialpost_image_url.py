# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialpost',
            name='image_url',
            field=models.CharField(max_length=255, db_column=b'image_url', blank=True),
        ),
    ]
