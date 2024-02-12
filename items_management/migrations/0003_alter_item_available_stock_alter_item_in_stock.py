# Generated by Django 5.0.2 on 2024-02-12 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items_management', '0002_populate_initial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='available_stock',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='item',
            name='in_stock',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
