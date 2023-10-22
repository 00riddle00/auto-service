# Generated by Django 4.2.6 on 2023-10-22 18:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0007_remove_orderline_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="car",
            name="description",
        ),
        migrations.AddField(
            model_name="car",
            name="observations",
            field=models.TextField(
                default="", max_length=2048, verbose_name="Observations"
            ),
        ),
    ]
