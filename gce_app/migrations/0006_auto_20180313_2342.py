# Generated by Django 2.0 on 2018-03-13 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gce_app', '0005_auto_20180313_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichiercopie',
            name='emplacement_fichier',
            field=models.FileField(blank=True, db_column='emplacement_Fichier', null=True, upload_to='media/copies'),
        ),
        migrations.AlterField(
            model_name='fichiercorrection',
            name='emplacement_fichier',
            field=models.FileField(blank=True, db_column='emplacement_Fichier', null=True, upload_to='media/copies'),
        ),
    ]
