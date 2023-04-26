from typing import Type

from django.db.models import QuerySet
from rest_framework import viewsets, mixins, permissions
from rest_framework.serializers import Serializer

from payment.models import Payment
from payment.serializers import PaymentListSerializer, PaymentDetailSerializer


class PaymentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self) -> Type[Serializer]:
        """Return serializer depending on the action"""
        if self.action == "retrieve":
            return PaymentDetailSerializer

    def get_queryset(self) -> QuerySet:
        """
        Return queryset all payment if user is admin,
        or filter payments by user.
        """
        if not self.request.user.is_staff:
            queryset = Payment.objects.filter(users=self.request.user)
        return self.queryset
