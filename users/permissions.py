from rest_framework import permissions
from .models import ProjectMembership
from rest_framework.exceptions import PermissionDenied


class IsOwnerManagerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        manager = obj.role == "manager"  
              
        if request.user == obj.project.owner or manager:
            return True
        
        raise PermissionDenied("Only OwnerOrManager can acces this.") 

    

# ProjectMembership
class IsOwnerManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_manager = obj.role == "manager"
        is_owner = obj.project.owner == request.user  

        if is_owner or is_manager:
            return True
        raise PermissionDenied("Only OwnerOrManager can acces this.") 
    
    
# class IsOwnerManagerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         manager = obj.role == "manager"
        
#         if not request.user and obj.project.owner or manager:
#             raise PermissionDenied("You Are Not Authorized To Add/Delete Members.") 
#         return True
    
# if not condition:
#     loginc

class ManagerRolePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is a manager of the project / Or even I don't need to check  this because this is 100% manager
        # | Ops it could be for owner so yeah we need        
        if obj.role == 'manager':
            # Prevent changing the role to 'manager'
            if 'role' in request.data and request.data['role'] == "manager":
                raise PermissionDenied("You cannot assign the role to 'manager''........................")

        return True
    
#done2
class ManagerRolePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is a manager of the project / Or even I don't need to check  this because this is 100% manager
        # | Ops it could be for owner so yeah we need    
        
        owner =  obj.project.owner
        
        if owner != request.user:
            if not obj.role == 'manager':
                # Prevent changing the role to 'manager'
                if 'role' in request.data and request.data['role'] == "manager":
                    raise PermissionDenied("You cannot assign the role to 'manager''........................")
            return True
            

        return True
# done2 | ProjectMembership
class ManagerAccPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is trying to delete a manager
        is_owner = obj.project.owner == request.user  

        if not is_owner:
            if obj.role == "manager":
                raise PermissionDenied("You can't play with manager Account")
        return True
    
    
    # Rough WOrk
    
# class IsOwnerManagerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # obj is already a ProjectMembership instance
#         # So check project memberships for this project
#         print('Before Manger')
#         manager = ProjectMembership.objects.filter(
#             project=obj.project,
#             employee=request.user,
#             role='manager'
#         ).exists()
#         print('After Manger')
        

#         return request.user == obj.project.owner or manager


#done2 |  PorjectMembership
class IsOwnerManagerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        manager = obj.role == "manager"  
              
        if request.user == obj.project.owner or manager:
            return True
        
        raise PermissionDenied("Only OwnerOrManager can acces this.") 

