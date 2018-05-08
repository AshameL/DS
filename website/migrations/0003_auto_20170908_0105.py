# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_referencefile_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testquestion',
            name='difficult',
            field=models.IntegerField(null=True),
        ),
    ]
