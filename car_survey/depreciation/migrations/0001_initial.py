# Generated by Django 5.1.3 on 2024-11-12 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50)),
                ('maker', models.CharField(max_length=50)),
                ('odometer', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
        ),
    ]