from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request: Request, view: object) -> bool:
        return bool(request.method in SAFE_METHODS or request.user.is_staff)
