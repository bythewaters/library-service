from rest_framework import serializers

from borrowing.models import Borrowing


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
    books = serializers.SlugRelatedField(
        read_only=True,
        slug_field="title",
    )
    users = serializers.SlugRelatedField(
        read_only=True,
        slug_field="email"
    )
