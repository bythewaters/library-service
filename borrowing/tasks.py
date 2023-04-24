from borrowing.models import Borrowing

from celery import shared_task


@shared_task
def count_borrowing():
    return Borrowing.objects.count()
