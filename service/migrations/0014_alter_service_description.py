# Generated by Django 4.2.6 on 2023-10-28 17:01

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0013_alter_carmodel_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="description",
            field=tinymce.models.HTMLField(
                default="", max_length=4096, verbose_name="Description"
            ),
        ),
    ]
