from django.core.exceptions import ValidationError
from django.db import models

from books.models import Book
from library_service import settings
from django.utils.translation import gettext_lazy as _


class Borrowing(models.Model):
    borrow_date = models.DateTimeField()
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )

    def clean(self) -> None:
        if self.borrow_date > self.expected_return_date:
            raise ValidationError(_("Expected return date must be after borrow date."))

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)
