# Generated by Django 3.0.4 on 2020-08-29 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodiagnosis', '0004_correlated_resport_report'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Correlated_Resport',
            new_name='Correlated_Report',
        ),
    ]