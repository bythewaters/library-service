# Generated by Django 4.2 on 2023-04-25 06:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("borrowing", "0006_alter_borrowing_borrow_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="borrow_date",
            field=models.DateTimeField(),
        ),
    ]