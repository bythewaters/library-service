# Generated by Django 4.2 on 2023-04-25 21:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("borrowing", "0010_alter_borrowing_borrow_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="expected_return_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 26, 21, 39, 6, 614067)
            ),
        ),
    ]