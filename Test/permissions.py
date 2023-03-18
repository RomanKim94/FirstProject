from rest_framework.permissions import BasePermission


class IsOwnerOrAdminOrCreateAnswerPermission(BasePermission):
    """Only Admin may update answer"""

    def has_permission(self, request, view):
        return bool(
            (view.action in ['update', 'partial_update'] and request.user and request.user.is_staff) or
            (view.action not in ['update', 'partial_update'] and request.user and request.user.is_authenticated)
            )

    def has_object_permission(self, request, view, obj):
        return bool(obj.trying.person
                    == request.user or
                    request.user.is_staff)


class IsOwnerOrAdminOrCreatePersonPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(obj == request.user or
                    request.user and request.user.is_staff or
                    not request.user and view.action == 'create')


class IsOwnerOrAdminTryingPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(obj.person == request.user or
                    request.user.is_staff or
                    request.user and view.action == 'create')


class IsAdminQuestionPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(
            view.action in ['list', 'retrieve'] or
            request.user and request.user.is_staff
        )
