from django.contrib import admin
from django.contrib.admin import ModelAdmin

from payment.models import Payment


@admin.register(Payment)
class FeedBackAdmin(ModelAdmin):
    list_display = (
        "status",
        "type",
        "borrowing",
        "session_url",
        "session_id",
        "money_to_pay",
    )
    ordering = ("status",)
