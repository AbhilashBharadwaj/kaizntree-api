# Generated by Django 5.0.2 on 2024-02-10 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("SKU", models.CharField(max_length=50, unique=True)),
                ("name", models.CharField(max_length=200)),
                (
                    "stock_status",
                    models.CharField(
                        choices=[
                            ("IN", "In Stock"),
                            ("OUT", "Out of Stock"),
                            ("BO", "Backorder"),
                        ],
                        default="IN",
                        max_length=3,
                    ),
                ),
                ("in_stock", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "available_stock",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="items",
                        to="items_management.category",
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="items_management.tag")),
            ],
        ),
    ]
