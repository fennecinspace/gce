# Generated by Django 2.0 on 2018-03-11 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gce_app', '0002_auto_20180310_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chefdepartement',
            name='modules',
        ),
        migrations.RemoveField(
            model_name='etudiant',
            name='modules',
        ),
    ]