from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSelfOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        #这个权限类和之前写过的类似，确保非安全方法只能由本人操作。
        return obj == request.user