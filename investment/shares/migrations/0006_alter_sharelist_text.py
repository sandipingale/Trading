# Generated by Django 4.1.5 on 2023-12-27 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shares", "0005_rename_symbol_sharelist_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sharelist",
            name="text",
            field=models.CharField(max_length=80),
        ),
    ]
