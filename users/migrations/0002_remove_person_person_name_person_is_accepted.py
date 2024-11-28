# Generated by Django 4.2.16 on 2024-11-22 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='person_name',
        ),
        migrations.AddField(
            model_name='person',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
    ]