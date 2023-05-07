# Generated by Django 4.2 on 2023-04-24 19:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("borrowing", "0003_alter_borrowing_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="borrow_date",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="borrowing",
            name="expected_return_date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
