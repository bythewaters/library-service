from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models

from books.models import Book
from library_service import settings


class Borrowing(models.Model):
    borrow_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)
    users = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    @staticmethod
    def validate_date(
            borrow_date: datetime, expected_return_date, error_to_raise
    ):
        if borrow_date > expected_return_date:
            raise error_to_raise(
                    "Expected return date must be after borrow date."
            )

    def clean(self) -> None:
        Borrowing.validate_date(
            self.borrow_date, self.expected_return_date, ValidationError
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )
