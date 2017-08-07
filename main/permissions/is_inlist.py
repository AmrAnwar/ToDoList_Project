from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsInList(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        check if user in list obj or not
        :param request:
        :param view:
        :param obj: List obj
        :return:
        """
        return request.user in obj.users.all()
