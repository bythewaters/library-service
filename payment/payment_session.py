import datetime
from typing import Union, Tuple
from unicodedata import decimal

import stripe
from rest_framework.response import Response
from rest_framework.reverse import reverse

from borrowing.models import Borrowing
from library_service import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
FINE_MULTIPLIER = 2


def create_payment_session(
    borrowing: Borrowing,
) -> Union[Tuple[str, str, decimal], Response]:
    message = borrowing.book.author
    borrow_price = (
        borrowing.expected_return_date - borrowing.borrow_date
    ).days * borrowing.book.daily_fee
    if borrowing.expected_return_date < datetime.date.today():
        fine_price = (
            (datetime.date.today() - borrowing.expected_return_date).days
            * borrowing.book.daily_fee
            * FINE_MULTIPLIER
        )
        borrow_price += fine_price
        message = f"You overdue borrowing. You're fine price: {fine_price} $"

    success_url = reverse("payment:success")
    cancel_url = reverse("payment:cancel")
    payment_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(borrow_price * 100),
                    "product_data": {
                        "name": borrowing.book.title,
                        "description": message,
                    },
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        metadata={"borrow_id": borrowing.id},
        success_url=settings.PAYMENT_SUCCESS_URL
        + success_url
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=settings.PAYMENT_FAILED_URL
        + cancel_url
        + "?session_id={CHECKOUT_SESSION_ID}",
    )
    return payment_session.url, payment_session.id, borrow_price
