# Generated by Django 5.1.3 on 2024-11-15 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fmv', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_price', models.IntegerField()),
                ('highest_value', models.IntegerField()),
                ('lowest_value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50)),
                ('maker', models.CharField(max_length=50)),
                ('transmission', models.CharField(max_length=10)),
                ('year', models.IntegerField()),
                ('odometer', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='UserInput',
        ),
    ]
