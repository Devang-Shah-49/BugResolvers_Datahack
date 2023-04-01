# Generated by Django 4.1.7 on 2023-04-01 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("basket", "0006_alter_order_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_date",
            field=models.DateField(),
        ),
        migrations.AlterUniqueTogether(
            name="order",
            unique_together={("order_id", "order_date")},
        ),
    ]
