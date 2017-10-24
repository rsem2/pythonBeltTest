# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 22:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('alias', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=50)),
                ('DoB', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserFriends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='users_app.User')),
                ('friend_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to='users_app.User')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='friends_of', through='users_app.UserFriends', to='users_app.User'),
        ),
    ]