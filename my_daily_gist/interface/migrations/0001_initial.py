# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255, db_column=b'description', blank=True)),
                ('post_id', models.CharField(max_length=255, db_column=b'post_id', blank=True)),
                ('post_type', models.PositiveIntegerField(default=0, db_column=b'post_type')),
            ],
            options={
                'db_table': 'social_posts',
            },
        ),
    ]
