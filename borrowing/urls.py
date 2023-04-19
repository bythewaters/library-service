from django.urls import path, include
from rest_framework import routers

from borrowing.views import BorrowingViewSet, BorrowingCreateViewSet

router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet)
router.register("borrowing/create", BorrowingCreateViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "borrowing"
