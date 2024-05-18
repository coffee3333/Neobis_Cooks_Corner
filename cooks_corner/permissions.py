from rest_framework import permissions

class ReadOnlyOrCreateOnlyAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        # Разрешить GET, HEAD, OPTIONS для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешить POST только аутентифицированным пользователям
        elif request.method == 'POST':
            return request.user and request.user.is_authenticated
        return False