# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dateme_app', '0002_auto_20150115_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagechallenge',
            name='isComplete',
            field=models.BooleanField(),
            preserve_default=True,
        ),
    ]
