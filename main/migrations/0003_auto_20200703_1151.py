# Generated by Django 3.0.4 on 2020-07-03 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200703_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='phone_number1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='phone_number2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]