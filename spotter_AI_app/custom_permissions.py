from rest_framework.permissions import BasePermission
class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        #print(request.user.is_authenticated)
        if "_auth_user_id"  in request.session.keys():
            return True
        return False
    