# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('value', models.CharField(unique=True, max_length=255)),
                ('level', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.DecimalField(max_digits=13, decimal_places=10)),
                ('longitude', models.DecimalField(max_digits=13, decimal_places=10)),
                ('timestamp', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('value', models.TextField()),
                ('contentType', models.ForeignKey(to='dateme_app.ContentType')),
                ('conversation', models.ForeignKey(to='dateme_app.Conversation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageChallenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.TextField(blank=True)),
                ('isComplete', models.BooleanField()),
                ('challenge', models.ForeignKey(to='dateme_app.Challenge')),
                ('message', models.ForeignKey(to='dateme_app.Message')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=100)),
                ('handle', models.CharField(max_length=35)),
                ('token', models.CharField(max_length=200)),
                ('token_expiration', models.DateTimeField()),
                ('tagline', models.CharField(max_length=300, blank=True)),
                ('birthday', models.DateField()),
                ('age_start', models.IntegerField()),
                ('age_end', models.IntegerField()),
                ('age', models.IntegerField()),
                ('gender', models.ForeignKey(related_name='gender', to='dateme_app.Gender')),
                ('orientation', models.ForeignKey(related_name='orientation', to='dateme_app.Gender')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=128)),
                ('user', models.ForeignKey(to='dateme_app.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('user', models.ForeignKey(to='dateme_app.Person')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='setting',
            unique_together=set([('user', 'name')]),
        ),
        migrations.AddField(
            model_name='messagechallenge',
            name='user',
            field=models.ForeignKey(to='dateme_app.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(to='dateme_app.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='user',
            field=models.ForeignKey(to='dateme_app.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conversation',
            name='people',
            field=models.ManyToManyField(to='dateme_app.Person'),
            preserve_default=True,
        ),
    ]
