# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('big', models.BooleanField(default=False)),
                ('clever', models.BooleanField(default=False)),
                ('count', models.IntegerField(default=0)),
                ('element_type', models.CharField(max_length=1, choices=[(b'e', b'Earth'), (b'w', b'Water'), (b'a', b'Air'), (b'f', b'Fire')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
