from rest_framework.permissions import BasePermission


class HasScope(BasePermission):
    def get_required_scope(self, view):
        return getattr(view, "required_scope", None)

    def has_permission(self, request, view):
        required = self.get_required_scope(view)
        if not required:
            return True
        actor = getattr(request, "actor", None)
        if actor is None:
            return False
        return actor.has_scope(required)


def scoped_permission(scope: str):
    class _ScopedPermission(HasScope):
        def get_required_scope(self, view):
            return scope

    return _ScopedPermission
