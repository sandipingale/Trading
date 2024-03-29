# Generated by Django 3.2.12 on 2022-03-19 02:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('savings', '0004_rename_user_bankaccount_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txn_type', models.CharField(choices=[('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')], max_length=10)),
                ('txn_amount', models.FloatField()),
                ('txn_category', models.CharField(choices=[('Utility', 'Utility'), ('Medicine', 'Medicine'), ('Automobile', 'Automobile'), ('Education', 'Education'), ('Entertainment', 'Entertainment'), ('Food', 'Food'), ('Groceries', 'Groceries'), ('Tax', 'Tax')], max_length=20)),
                ('bank_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='savings.bankaccount')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
