from rest_framework import permissions

class CustomUserPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        """
        Overwrites permissions for user on leads objects
        """
        if not request.user.is_authenticated:
            return False

        else:
            return True

    def has_object_permission(self, request, view, obj):
        """
        Overwrites user permissions on leads object
        """
        if not request.user.is_authenticated:
            return False

        elif request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user or request.user.is_superuser