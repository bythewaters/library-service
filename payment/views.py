from typing import Type

import stripe
from django.db.models import QuerySet
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from payment.models import Payment
from payment.serializers import PaymentListSerializer, PaymentDetailSerializer


class PaymentViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self) -> Type[Serializer]:
        """Return serializer depending on the action"""
        if self.action == "retrieve":
            return PaymentDetailSerializer
        return self.serializer_class

    def get_queryset(self) -> QuerySet:
        """
        Return queryset all payment if user is admin,
        or filter payments by user.
        """
        if not self.request.user.is_staff:
            return Payment.objects.filter(borrowing__user=self.request.user)
        return self.queryset

    @action(
        methods=["GET"],
        url_name="success",
        detail=False,
    )
    def success(self, request: Request) -> Response:
        """Action for success payment"""
        session_id = request.query_params.get("session_id", False)
        payment = Payment.objects.get(session_id=session_id)
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == "paid":
            serializer = PaymentDetailSerializer(
                payment, data={"status": "PAID"}, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {
                "status": "error",
                "message": "Payment not success",
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=["GET"],
        url_name="cancel",
        detail=False,
    )
    def cancel(self, request: Request) -> Response:
        """Action for not success payment"""
        session_id = request.query_params.get("session_id", False)
        session = stripe.checkout.Session.retrieve(session_id)
        if not session.payment_status == "PAID":
            return Response(
                {
                    "status": "Cancel payment",
                    "message": "You can be paid a bit later "
                               "(but the session is available for only 24h)",
                },
                status=status.HTTP_303_SEE_OTHER
            )
