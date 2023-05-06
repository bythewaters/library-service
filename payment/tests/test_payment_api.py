from datetime import date, timedelta

from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from books.models import Book
from borrowing.models import Borrowing
from library_service import settings
from payment.models import Payment
from payment.payment_session import create_payment_session
from users.models import User
from unittest.mock import patch, Mock


class CreatePaymentSessionTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test_user@example.com", password="password"
        )
        self.client.force_authenticate(self.user)

    def test_create_payment_session(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Soft",
            inventory=1,
            daily_fee=9.99,
        )
        borrowing = Borrowing.objects.create(
            books=book,
            users=self.user,
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=2),
            actual_return_date=None,
        )

        mock_session = Mock(
            id="test_session_id",
            url="http://test-session-url.com",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": 9.99,
                        "product_data": {
                            "name": borrowing.books.title,
                            "description": "Book borrowing fee",
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_FAILED_URL,
        )

        with patch(
                "stripe.checkout.Session.create",
                return_value=mock_session
        ):
            session_url, session_id, borrow_price = create_payment_session(
                borrowing
            )

        payment = Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            borrowing=borrowing,
            session_url=session_url,
            session_id=session_id,
            money_to_pay=borrow_price,
        )
        self.assertEqual(session_id, "test_session_id")
        self.assertEqual(session_url, "http://test-session-url.com")
        payment.refresh_from_db()
        self.assertEqual(payment.status, "PENDING")
        self.assertEqual(payment.type, "PAYMENT")
        self.assertEqual(payment.borrowing, borrowing)
        self.assertEqual(float(payment.money_to_pay), borrow_price)
        self.assertEqual(
            settings.PAYMENT_SUCCESS_URL + reverse("payment:success"),
            "http://localhost:8000/api/library/payment/success/",
        )
        self.assertEqual(
            settings.PAYMENT_FAILED_URL + reverse("payment:cancel"),
            "http://localhost:8000/api/library/payment/cancel/",
        )
