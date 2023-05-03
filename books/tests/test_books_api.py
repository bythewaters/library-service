from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from books.models import Book
from books.serializers import BookSerializer


BOOKS_URL = reverse("books:book-list")


def sample_book(**params):
    defaults = {
        "title": "Test",
        "author": "TestAuthor",
        "cover": "HARD",
        "inventory": 4,
        "daily_fee": 0.16
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


class NotStaffUsersApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_books(self):
        sample_book()
        sample_book()

        res = self.client.get(BOOKS_URL)

        books = Book.objects.order_by("id")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_forbidden_create_book(self):
        data = {
            "title": "Test",
            "author": "TestAuthor",
            "cover": "HARD",
            "inventory": 4,
            "daily_fee": 0.16
        }
        res = self.client.post(data=data, path=BOOKS_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_update_book(self):
        book = sample_book()
        data = {
            "title": "AnotherTitle"
        }
        res = self.client.patch(path=BOOKS_URL + f"{book.id}/", data=data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class StaffUsersApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.user.is_staff = True
        self.client.force_authenticate(self.user)

    def test_list_books(self):
        sample_book()
        sample_book()

        res = self.client.get(BOOKS_URL)

        books = Book.objects.order_by("id")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_forbidden_create_book(self):
        data = {
            "title": "Test",
            "author": "TestAuthor",
            "cover": "HARD",
            "inventory": 4,
            "daily_fee": 0.16
        }
        res = self.client.post(data=data, path=BOOKS_URL)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_forbidden_update_book(self):
        book = sample_book()
        data = {
            "title": "AnotherTitle"
        }
        res = self.client.patch(path=BOOKS_URL + f"{book.id}/", data=data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
