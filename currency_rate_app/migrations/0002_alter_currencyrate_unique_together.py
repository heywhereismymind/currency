# Generated by Django 4.2.7 on 2023-11-14 20:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("currency_rate_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="currencyrate",
            unique_together=set(),
        ),
    ]
