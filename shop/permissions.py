from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        # Read or Write permissions are only allowed to the owner of the order or superuser.
        return obj.owner == request.user or request.user.is_superuser
