# Generated by Django 3.0.4 on 2020-07-08 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autodiagnosis', '0002_auto_20200708_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500, null=True)),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autodiagnosis.Origin')),
            ],
        ),
    ]
