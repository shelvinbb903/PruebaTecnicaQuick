# Generated by Django 2.2.13 on 2022-05-15 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=150)),
                ('price', models.DecimalField(decimal_places=2, max_digits=18)),
            ],
            options={
                'db_table': 'products',
            },
        ),
    ]