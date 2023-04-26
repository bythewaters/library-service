from django.db.models import Q
from django.utils import timezone

from borrowing.models import Borrowing
from celery import shared_task
from notifications.telegram_notification import send_to_telegram


@shared_task
def check_borrowing_overdue():
    """The function filter all borrowings,
    which are overdue
    and send a notification to the telegram chat
    about each overdue separately with detailed information
    """
    today = timezone.now()
    overdue_borrowing = Borrowing.objects.filter(
        Q(expected_return_date__lte=today) & Q(actual_return_date__isnull=True)
    )

    for borrowing in overdue_borrowing:
        message = (
            f"The borrowing of the book"
            f"{borrowing.books.title} by {borrowing.users.first_name}"
            f"is overdue.\n The expected return date was\n"
            f"{borrowing.expected_return_date}."
        )
        send_to_telegram(message)
