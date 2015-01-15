# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dateme_app', '0003_auto_20150115_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagechallenge',
            name='isComplete',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
