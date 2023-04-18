from django.db import models

from books.models import Book
from library_service import settings


class Borrowing(models.Model):
    borrow_date = models.DateTimeField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )
