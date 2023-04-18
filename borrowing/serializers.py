from rest_framework import serializers
from books.serializers import BookSerializer
from borrowing.models import Borrowing
from users.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "users",
            "books",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        ]


class BorrowingDetailSerializer(BorrowingSerializer):
    books = BookSerializer(
        read_only=True,
    )
    users = UserSerializer(
        read_only=True,
    )
