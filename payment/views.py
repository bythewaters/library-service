from typing import Type

from rest_framework import viewsets, mixins
from rest_framework.serializers import Serializer

from payment.models import Payment
from payment.serializers import PaymentListSerializer, PaymentDetailSerializer


class PaymentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return PaymentDetailSerializer
