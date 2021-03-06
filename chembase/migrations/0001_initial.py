# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-27 11:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annotation', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cmpd_Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Compound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('all_names', models.CharField(blank=True, max_length=5000)),
                ('subtitle', models.CharField(blank=True, max_length=1000)),
                ('cas', models.CharField(blank=True, max_length=100, verbose_name='CAS')),
                ('csid', models.CharField(blank=True, max_length=15, verbose_name='ChemSpider Id')),
                ('formula', models.CharField(blank=True, max_length=100)),
                ('weight', models.DecimalField(blank=True, decimal_places=3, max_digits=10, verbose_name='Molecular weight')),
                ('density', models.DecimalField(blank=True, decimal_places=2, max_digits=6)),
                ('image', models.FilePathField(blank=True, max_length=200)),
                ('inchi', models.CharField(blank=True, max_length=1000, verbose_name='InChi')),
                ('smiles', models.CharField(blank=True, max_length=1000, verbose_name='SMILES')),
                ('sds', models.FilePathField(blank=True, max_length=200, verbose_name='SDS')),
                ('sds_name', models.CharField(blank=True, max_length=2000)),
                ('sds_cas', models.CharField(blank=True, max_length=100)),
                ('warning', models.CharField(blank=True, max_length=200)),
                ('h_numbers', models.CharField(blank=True, max_length=2000)),
                ('h_text', models.TextField(blank=True)),
                ('p_numbers', models.CharField(blank=True, max_length=2000)),
                ('p_text', models.TextField(blank=True)),
                ('classification', models.TextField(blank=True)),
                ('adr_num', models.CharField(blank=True, max_length=15)),
                ('adr_class', models.CharField(blank=True, max_length=15)),
                ('adr_group', models.CharField(blank=True, max_length=15)),
                ('dailyused', models.CharField(blank=True, max_length=15, verbose_name='Daily usage')),
            ],
        ),
        migrations.CreateModel(
            name='Ewidencja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('compound', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chembase.Compound')),
            ],
        ),
        migrations.CreateModel(
            name='GHSClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='H_Pict_Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h_code', models.CharField(max_length=8)),
                ('ghs_class', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chembase.GHSClass')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('action', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=20)),
                ('place', models.CharField(max_length=20)),
                ('place_num', models.CharField(max_length=20)),
                ('quantity', models.IntegerField(blank=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=3, max_digits=10)),
                ('storage_temp', models.CharField(blank=True, max_length=10)),
                ('hidden', models.BooleanField()),
                ('compound', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chembase.Compound')),
            ],
        ),
        migrations.CreateModel(
            name='Pictogram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('path', models.FilePathField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='history',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chembase.Item'),
        ),
        migrations.AddField(
            model_name='h_pict_class',
            name='pictogram',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chembase.Pictogram'),
        ),
        migrations.AddField(
            model_name='compound',
            name='class_extr',
            field=models.ManyToManyField(through='chembase.Cmpd_Class', to='chembase.GHSClass'),
        ),
        migrations.AddField(
            model_name='compound',
            name='pictograms',
            field=models.ManyToManyField(to='chembase.Pictogram'),
        ),
        migrations.AddField(
            model_name='cmpd_class',
            name='compound',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chembase.Compound'),
        ),
        migrations.AddField(
            model_name='cmpd_class',
            name='ghs_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chembase.GHSClass'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chembase.Item'),
        ),
    ]
