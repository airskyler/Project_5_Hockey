# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-01 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opponent', models.TextField()),
                ('date', models.DateTimeField()),
                ('homeVSaway', models.CharField(choices=[('H', 'Home'), ('A', 'Away')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Merchandise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SoldItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberSold', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchandise.Game')),
                ('merch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchandise.Merchandise')),
            ],
        ),
    ]
