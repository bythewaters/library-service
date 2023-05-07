from rest_framework import serializers

from borrowing.serializers import BorrowingDetailSerializer
from payment.models import Payment


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        ]


class PaymentDetailSerializer(PaymentListSerializer):
    borrowing = BorrowingDetailSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        ]
