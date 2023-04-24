from borrowing.models import Borrowing

from celery import shared_task


@shared_task
def check_borrowing_overdue():
    """The function filter all borrowings,
    which are overdue
    and send a notification to the telegram chat
    about each overdue separately with detailed information
    """
    check_borrowing = Borrowing.objects.filter()
