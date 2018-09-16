# Generated by Django 2.1.1 on 2018-09-16 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LinkStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Scanning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Stop'), (1, 'Run')], default=0)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TokenStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=128, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
