# Generated by Django 4.2 on 2023-04-25 21:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("borrowing", "0009_alter_borrowing_borrow_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="borrow_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterUniqueTogether(
            name="borrowing",
            unique_together={
                ("borrow_date", "expected_return_date", "actual_return_date")
            },
        ),
    ]
