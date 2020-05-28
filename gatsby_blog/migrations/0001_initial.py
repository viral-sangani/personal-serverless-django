# Generated by Django 3.0.6 on 2020-05-26 14:36

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import gatsby_blog.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=500)),
                ('totalLikes', models.IntegerField(default=0)),
                ('individualLikes', django.contrib.postgres.fields.jsonb.JSONField(default=gatsby_blog.models.default)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('ipList', django.contrib.postgres.fields.jsonb.JSONField(default=gatsby_blog.models.default)),
            ],
        ),
    ]