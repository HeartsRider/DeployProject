# Generated by Django 2.2 on 2023-02-11 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatGPT3RequestorModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apikey', models.CharField(max_length=100)),
                ('payload', models.CharField(max_length=100)),
            ],
        ),
    ]