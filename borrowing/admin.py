from django.contrib import admin
from django.contrib.admin import ModelAdmin

from borrowing.models import Borrowing


@admin.register(Borrowing)
class FeedBackAdmin(ModelAdmin):
    list_display = (
        "users",
        "books",
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
    )
    ordering = ("borrow_date",)
