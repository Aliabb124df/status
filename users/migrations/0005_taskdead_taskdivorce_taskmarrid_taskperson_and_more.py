# Generated by Django 4.2.16 on 2024-11-23 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_marrid_image_marrid_is_accepted'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskDead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('national_num', models.CharField(max_length=15)),
                ('place_of_death', models.CharField(max_length=15)),
                ('date_of_death', models.DateField(null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/%y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='TaskDivorce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('national_hus', models.CharField(max_length=15)),
                ('national_wife', models.CharField(max_length=15)),
                ('date_of_divorce', models.DateField(null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/%y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='TaskMarrid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('national_hus', models.CharField(max_length=15)),
                ('national_wife', models.CharField(max_length=15, unique=True)),
                ('date_of_marrid', models.DateField(null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/%y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='TaskPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(max_length=15, null=True, unique=True)),
                ('national_num', models.CharField(max_length=15, unique=True)),
                ('first_name', models.CharField(max_length=15, null=True)),
                ('last_name', models.CharField(max_length=15, null=True)),
                ('national_dad', models.CharField(max_length=15, null=True)),
                ('national_mom', models.CharField(max_length=15, null=True)),
                ('birth_place', models.CharField(max_length=15, null=True)),
                ('birth_date', models.DateField(null=True)),
                ('date_of_issue', models.DateField(null=True)),
                ('place_of_issue', models.CharField(max_length=15, null=True)),
                ('number_of_issue', models.IntegerField(null=True)),
                ('religion', models.CharField(choices=[('muslim', 'muslim'), ('Christian', 'Christian')], default='muslim', max_length=9)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=7)),
                ('status', models.CharField(choices=[('single', 'single'), ('married', 'married'), ('divorced', 'divorced'), ('widower', 'widower')], default='single', max_length=8)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/%y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='TaskWidower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('national_hus', models.CharField(max_length=15)),
                ('national_wife', models.CharField(max_length=15)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/%y/%m/%d')),
            ],
        ),
        migrations.DeleteModel(
            name='Cfile',
        ),
        migrations.RemoveField(
            model_name='marrid',
            name='is_accepted',
        ),
        migrations.RemoveField(
            model_name='person',
            name='is_accepted',
        ),
        migrations.AddField(
            model_name='marrid',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/%y/%m/%d'),
        ),
    ]
