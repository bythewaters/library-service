from django.db import transaction
from rest_framework import serializers
from books.serializers import BookSerializer
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
    books = BookSerializer(
        read_only=True,
    )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    def validate(self, validated_data: dict) -> dict:
        data = super(
            BorrowingCreateSerializer, self
        ).validate(attrs=validated_data)
        Borrowing.validate_date(
            validated_data["borrow_date"],
            validated_data["expected_return_date"],
            serializers.ValidationError,
        )

        book = validated_data.get("books")
        if not book:
            raise serializers.ValidationError("Book is required.")

        if book.inventory <= 0:
            raise serializers.ValidationError(
                {"Books_error": "Book is not available for borrowing."}
            )
        return data

    class Meta:
        model = Borrowing
        fields = [
            "books",
            "borrow_date",
            "expected_return_date",
        ]

    @transaction.atomic
    def create(self, validated_data: dict) -> Borrowing:
        book = validated_data["books"]
        book.inventory -= 1
        book.save()
        borrowing = Borrowing.objects.create(**validated_data)
        return borrowing


class BorrowingReturnBookSerializer(BorrowingSerializer):

    class Meta:
        model = Borrowing
        fields = ["actual_return_date"]

    def validate(self, attrs: dict) -> dict:
        actual_return_date = attrs["actual_return_date"]

        if actual_return_date:
            raise serializers.ValidationError(
                {"Borrowings": "This book already returned"}
            )
        return attrs
