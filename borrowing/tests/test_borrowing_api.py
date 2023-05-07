from datetime import date, timedelta

from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from books.models import Book
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
)

BORROWINGS_URL = reverse("borrowings:borrowing-list")


def sample_borrowing(**params):
    book = Book.objects.create(
        title="BookTest",
        author="TestAuthor",
        cover="HARD",
        inventory=4,
        daily_fee=0.17
    )

    defaults = {
        "borrow_date": date.today(),
        "expected_return_date": date.today() + timedelta(days=10),
        "actual_return_date": None,
        "book": book,
        "user": None,
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWINGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test3.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_borrowings(self):
        book = Book.objects.create(
            title="BookTest2",
            author="TestAuthor2",
            cover="HARD",
            inventory=4,
            daily_fee=0.17,
        )

        sample_borrowing(user=self.user)
        sample_borrowing(user=self.user, book=book)

        res = self.client.get(BORROWINGS_URL)

        movies = Borrowing.objects.order_by("id")
        serializer = BorrowingSerializer(movies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_borrowings_by_active(self):
        book = Book.objects.create(
            title="BookTest2",
            author="TestAuthor2",
            cover="HARD",
            inventory=4,
            daily_fee=0.17,
        )

        borrowing1 = sample_borrowing(
            user=self.user,
            actual_return_date=date.today() + timedelta(days=5)
        )
        borrowing2 = sample_borrowing(user=self.user, book=book)
        res = self.client.get(BORROWINGS_URL, {"is_active": "true"})

        serializer1 = BorrowingSerializer(borrowing1)
        serializer2 = BorrowingSerializer(borrowing2)

        self.assertNotIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)

    def test_retrieve_borrowing_detail(self):
        borrowing = sample_borrowing(user=self.user)
        res = self.client.get(BORROWINGS_URL + f"{borrowing.id}/")
        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_borrowing(self):
        book = Book.objects.create(
            title="BookTest",
            author="TestAuthor",
            cover="HARD",
            inventory=4,
            daily_fee=0.17,
        )

        defaults = {
            "expected_return_date": date.today() + timedelta(days=10),
            "book": book.id,
        }
        res = self.client.post(path=BORROWINGS_URL, data=defaults)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_decrease_book_inventory_after_create_borrowing(self):
        book = Book.objects.create(
            title="BookTest",
            author="TestAuthor",
            cover="HARD",
            inventory=4,
            daily_fee=0.17,
        )
        defaults = {
            "expected_return_date": date.today() + timedelta(days=10),
            "book": book.id,
        }
        res = self.client.post(path=BORROWINGS_URL, data=defaults)
        book2 = Borrowing.objects.get(book=book)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(book2.book.inventory, book.inventory)

    def test_increase_book_inventory_after_return_book(self):
        book = Book.objects.create(
            title="BookTest",
            author="TestAuthor",
            cover="HARD",
            inventory=4,
            daily_fee=0.17,
        )
        defaults = {
            "expected_return_date": date.today() + timedelta(days=10),
            "book": book.id,
        }
        self.client.post(path=BORROWINGS_URL, data=defaults)
        borrowing = Borrowing.objects.get(book=book)
        self.assertNotEqual(book.inventory, borrowing.book.inventory)
        res = self.client.patch(
            path=BORROWINGS_URL + f"{borrowing.id}/return/",
            data={"actual_return_date": date.today() + timedelta(days=7)},
        )
        borrowing.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(book.inventory, borrowing.book.inventory)


class AdminBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "password",
        )
        self.client.force_authenticate(self.user)
        self.user.is_staff = True

    def test_list_borrowings_all_users(self):
        user1 = get_user_model().objects.create_user(
            "test@test1.com",
            "password1",
        )
        user2 = get_user_model().objects.create_user(
            "test@test2.com",
            "password2",
        )
        sample_borrowing(user=user1)
        sample_borrowing(user=user2)
        res = self.client.get(BORROWINGS_URL)
        borrowings = Borrowing.objects.order_by("id")
        serializer = BorrowingSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_borrowings_by_user_id(self):
        book1 = Book.objects.create(
            title="BookTest2",
            author="TestAuthor2",
            cover="HARD",
            inventory=4,
            daily_fee=0.17,
        )
        user = get_user_model().objects.create_user(
            "test123@gmail.com",
            "password1"
        )
        borrowing2 = sample_borrowing(user=user, book=book1)
        serializer2 = BorrowingSerializer(borrowing2)

        res = self.client.get(BORROWINGS_URL, {"user_id": user.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer2.data, res.data)
