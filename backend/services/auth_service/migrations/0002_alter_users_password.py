# Generated by Django 5.1.4 on 2024-12-27 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]