# Generated by Django 3.2.12 on 2022-03-18 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0002_alter_bankaccount_initial_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='balance',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='initial_balance',
            field=models.FloatField(),
        ),
    ]
