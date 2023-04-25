from datetime import date
from typing import Type, Optional

from django.core.exceptions import ValidationError
from django.db import models

from books.models import Book
from library_service import settings


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @staticmethod
    def validate_date(
        expected_return_date: date,
        actual_return_date: date,
        error_to_raise: Type[ValidationError],
    ):
        if expected_return_date < date.today():
            raise error_to_raise("Return date must be after borrow date!")

        if actual_return_date and actual_return_date <= date.today():
            raise error_to_raise(
                "Actual return date cannot be less or equal borrow date"
            )

    def clean(self) -> None:
        Borrowing.validate_date(
            self.expected_return_date,
            self.actual_return_date,
            ValidationError,
        )

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[list[str]] = None,
    ):
        self.full_clean()
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )
