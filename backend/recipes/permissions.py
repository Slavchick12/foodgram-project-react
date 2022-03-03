from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class AdminUserOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or (
                request.user == obj.author) or request.user.is_staff)
