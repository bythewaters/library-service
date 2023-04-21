from typing import Type

from django.db.models import QuerySet
from rest_framework import viewsets, mixins, permissions
from rest_framework.serializers import Serializer

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer, BorrowingCreateSerializer
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Borrowing]:
        return Borrowing.objects.filter(users=self.request.user)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        return self.serializer_class

    def perform_create(self, serializer: Serializer[Borrowing]) -> None:
        serializer.save(users=self.request.user)
