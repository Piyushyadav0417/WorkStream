from rest_framework import permissions

class IsOwnerCreatorAssigneeOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('Permissions1 are ccalling')
        if request.method in permissions.SAFE_METHODS:
            return True
        
        owner = obj.task_list.boards.project.owner == request.user
        creator = obj.created_by == request.user
        assignee = obj.assignments.filter(assigne_to=request.user).exists()
        return owner or creator or assignee
    
#Task
class IsOwnerTaskCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('Permissions1 are ccalling')
        if request.method in permissions.SAFE_METHODS:
            return True
        
        owner = obj.task_list.boards.project.owner == request.user
        creator = obj.created_by == request.user
        
        return owner or creator
    

class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'Only Project Owner Can Access This'
    def has_object_permission(self, request, view, obj):
        print('Permissions1 are ccalling')
        if request.method in permissions.SAFE_METHODS:
            return True
        print('Permissions are ccalling')
        print(f'checking users {obj.owner} == {request.user}')
        return obj.owner == request.user
    
class IsCreaterOwnerOrReadOnly(permissions.BasePermission):
    
    message = 'Only Project Owner&Manager can update the data.'
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.project.owner == request.user or obj.created_by == request.user
    # def has_object_permission(self, request, view, project, boards):
        # if project.owner == request.user:
        #     return True
        # if boards.created_by == request.user:
        #     return True
        
        # if obje.project.owner == request.user: only one object(board)
        
        # if obj.boards.created_by == request.user: (project)
        
        
class IsBoardsOwnerProjectOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            print("'It's not Safe Method ")
            return True
        
    # print('task board created_by',task.boards.created_by)
    # print('task board project owner',task.boards.project.owner)
        print('FOr creater',obj.boards.created_by)
        print('ANd')
        print('FOr owner',obj.boards.project.owner)

        return obj.boards.created_by == request.user or obj.boards.project.owner == request.user