# Generated by Django 4.2.16 on 2024-11-22 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_alter_document_document_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/%y/%m/%d'),
        ),
    ]