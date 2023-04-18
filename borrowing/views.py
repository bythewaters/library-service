from typing import Type

from rest_framework import viewsets
from rest_framework.serializers import Serializer

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action in ("list", "retrieve"):
            return self.serializer_class
        return BorrowingDetailSerializer
