# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('briefTitle', models.CharField(max_length=64)),
                ('briefContent', models.CharField(max_length=1024)),
                ('briefReleaseTime', models.DateTimeField(auto_now=True)),
                ('briefClass', models.CharField(max_length=16)),
                ('briefType', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chap_id', models.IntegerField()),
                ('chap_num', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classname', models.CharField(unique=True, max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='ErrorQue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('erroranswer', models.CharField(max_length=4)),
                ('count', models.IntegerField()),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.CharField(max_length=32)),
                ('accuracy', models.FloatField()),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReferenceFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=32)),
                ('uploadtime', models.DateTimeField(auto_now_add=True)),
                ('remark', models.CharField(null=True, max_length=64, blank=True)),
                ('path', models.CharField(max_length=128)),
                ('suffix', models.CharField(null=True, max_length=12)),
                ('chapter', models.ForeignKey(null=True, to='website.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='TestQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=512)),
                ('A', models.CharField(max_length=128)),
                ('B', models.CharField(max_length=128)),
                ('C', models.CharField(null=True, max_length=128)),
                ('D', models.CharField(null=True, max_length=128)),
                ('difficult', models.IntegerField()),
                ('answer', models.CharField(max_length=2)),
                ('knowledge', models.CharField(max_length=16)),
                ('chapter', models.ForeignKey(to='website.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(unique=True, max_length=16)),
                ('name', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=16)),
                ('headImage', models.CharField(max_length=255)),
                ('type', models.IntegerField()),
                ('myclass', models.ForeignKey(null=True, to='website.Classes')),
            ],
        ),
        migrations.AddField(
            model_name='grade',
            name='userid',
            field=models.ForeignKey(to='website.User'),
        ),
        migrations.AddField(
            model_name='errorque',
            name='gradeid',
            field=models.ForeignKey(to='website.Grade'),
        ),
        migrations.AddField(
            model_name='errorque',
            name='testid',
            field=models.ForeignKey(to='website.TestQuestion'),
        ),
    ]
