from rest_framework.permissions import BasePermission
from rest_framework import permissions

#Obsolete
# class IsPostAuthor(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.author == request.user
    
class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
#New
class CanViewPost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        #Admin
        # if request.user.role =='ADMIN' or obj.author == request.user:
        if getattr(request.user, 'role', None) == 'ADMIN':
            return True
        #Restrict Delete to admin only
        if request.method == 'DELETE':
            return getattr(request.user, 'role', None) == 'ADMIN'
        
        if getattr(request.user, 'role', None) == 'ADMIN' or obj.author == request.user:
            return True
        
        #Author
        if obj.author == request.user:
            return True
        
        #Others
        if request.method in permissions.SAFE_METHODS:
            return obj.privacy == 'PUBLIC'
        return False
        
#Global RBAC Guest Restriction
class IsNotGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        return str(getattr(request.user, 'role', None)).upper() != 'GUEST'