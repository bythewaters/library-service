from typing import Type

from django.db.models import QuerySet
from rest_framework import viewsets, mixins, permissions
from rest_framework.serializers import Serializer

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Borrowing]:
        """
        Return borrowings only for current user.
        Filtering if borrowing has not returned yet.
        Admin can see all users borrowings, and filtering borrowing by user id.
        """
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = Borrowing.objects.filter(users=self.request.user)

        if self.request.user.is_staff:
            if user_id:
                queryset = queryset.filter(users_id=user_id)

        if is_active:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date=None)

        return queryset

    def get_serializer_class(self) -> Type[Serializer]:
        """Return serializer depending on the action"""
        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        return self.serializer_class

    def perform_create(self, serializer: Serializer[Borrowing]) -> None:
        """Create borrowing only for current user"""
        serializer.save(users=self.request.user)
