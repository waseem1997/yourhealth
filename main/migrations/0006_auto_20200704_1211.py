# Generated by Django 3.0.4 on 2020-07-04 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_appointment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='Patient',
            new_name='patient',
        ),
    ]
