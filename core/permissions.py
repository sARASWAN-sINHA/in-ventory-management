from rest_framework.permissions import BasePermission

class IsAssetAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Asset Admin").exists()

class IsAssetNormalUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Asset User").exists()

class IsAssetModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Asset Moderator").exists()
