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
    def validate(self, validated_data):
        book = validated_data.get("books")
        if not book:
            raise serializers.ValidationError("Book is required.")

        if book.inventory <= 0:
            raise serializers.ValidationError("Book is not available for borrowing.")
        return validated_data

    class Meta:
        model = Borrowing
        fields = [
            "users",
            "books",
            "borrow_date",
            "expected_return_date",
        ]

    @transaction.atomic
    def create(self, validated_data):
        book = validated_data["books"]
        book.inventory -= 1
        book.save()
        borrowing = Borrowing.objects.create(**validated_data)
        return borrowing
