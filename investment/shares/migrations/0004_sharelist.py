# Generated by Django 3.2.6 on 2021-08-21 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shares', '0003_auto_20210821_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]