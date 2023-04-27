from typing import Union, Tuple
from unicodedata import decimal

import stripe
from rest_framework.response import Response
from borrowing.models import Borrowing
from library_service import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_session(borrowing: Borrowing) -> Union[Tuple[str, str, decimal], Response]:
    borrow_price = (
        borrowing.expected_return_date - borrowing.borrow_date
    ).days * borrowing.books.daily_fee
    payment_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(borrow_price * 100),
                    "product_data": {
                        "name": borrowing.books.title,
                        "description": borrowing.books.author,
                    },
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        metadata={"borrow_id": borrowing.id},
        success_url=settings.PAYMENT_SUCCESS_URL,
        cancel_url=settings.PAYMENT_FAILED_URL,
    )
    return payment_session.url, payment_session.id, borrow_price
