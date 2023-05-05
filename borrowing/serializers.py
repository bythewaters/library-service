from django.db import transaction
from rest_framework import serializers
from books.serializers import BookSerializer
from borrowing.models import Borrowing
from notifications.telegram_notification import send_to_telegram
from payment.models import Payment
from payment.payment_session import create_payment_session


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
        data = super(BorrowingCreateSerializer, self).validate(validated_data)
        Borrowing.validate_date(
            validated_data.get("expected_return_date"),
            validated_data.get("actual_return_date"),
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
            "expected_return_date",
        ]

    @transaction.atomic
    def create(self, validated_data: dict) -> Borrowing:
        book = validated_data.get("books")
        expected_return_date = validated_data.get("expected_return_date")
        book.inventory -= 1
        book.save()
        borrowing = Borrowing.objects.create(**validated_data)
        borrow_date = borrowing.borrow_date
        session_url, session_id, borrow_price = create_payment_session(borrowing)
        Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            borrowing=borrowing,
            session_url=session_url,
            session_id=session_id,
            money_to_pay=borrow_price
        )
        send_to_telegram(
            f"Hello, you borrowed book: {book.title}.\n"
            f"Date borrow: {borrow_date}\n"
            f"Expected return date: {expected_return_date}\n"
            f"Price per day: {book.daily_fee} $\n"
            f"Thank you! Good Bye!"
        )
        return borrowing


class BorrowingReturnBookSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        fields = ["actual_return_date"]

    def validate(self, attrs: dict) -> dict:
        pk = self.context.get("pk")
        actual_return_date = attrs["actual_return_date"]
        borrowing = Borrowing.objects.get(id=pk)
        if borrowing.actual_return_date:
            raise serializers.ValidationError(
                {"Borrowings": "This book already returned"}
            )
        borrowing.actual_return_date = actual_return_date
        return attrs
