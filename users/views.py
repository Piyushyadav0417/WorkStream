from django.shortcuts import render, get_object_or_404
# from django.http import Http404
from .models import ProjectMembership, UserNotification
from notifications.models import ProjectJoinRequest
from notifications.views import send_mail_message
from projects.models import Project
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ProjectMembershipSerializer, UserNotificationSerializer
from .permissions import IsOwnerManagerOrReadOnly, ManagerRolePermission, ManagerAccPermission, IsOwnerManager 
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def users_temp(request):
    return render(request, 'users/users_temp.html')


# ProjectMembership|ProjectJoinRequest|--HTTP---DONE2
class ProjectMembershipAPI(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
#   get---------
    def get (self, request, project_id):
        if project_id:
            try:
                project = get_object_or_404(Project, id=project_id)
            except:
                return Response({f'No Project Exist with id: {project_id} '}, status=status.HTTP_404_NOT_FOUND)
            
        
        if project.is_private:
            if not project.owner == request.user:
                return Response({f'This Is a Private Project'}, status=status.HTTP_403_FORBIDDEN)
            
        members = ProjectMembership.objects.filter(project_id=project_id)
        
        username = request.query_params.get('user')
        if username:
            members = members.filter(user__username__istartswith=username)
            
        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginator_members = paginator.paginate_queryset(members, request)

        serializer = ProjectMembershipSerializer(paginator_members, many=True)
        return paginator.get_paginated_response(serializer.data)
           
    #post---------
    def post(self, request, project_id):
        try:
                
            project = get_object_or_404(Project, id=project_id)
        except:
            return Response({f'No Project Exist with id: {project_id} '}, status=status.HTTP_404_NOT_FOUND)
        
        if project.owner != request.user:
            try:
                #check current user exist in membership
                membership = get_object_or_404(ProjectMembership, user = request.user, project_id=project_id)
            except:
                return Response({f'You Are  Not Member of this Project'}, status=status.HTTP_403_FORBIDDEN)   
            
            # Cheacking IsOwnerManagerOrReadOnly can add members
            permission = IsOwnerManagerOrReadOnly()
            print('membership', membership)
            permission.has_object_permission(request, self, membership)

        
            # ManagerRolePermission he can assign all the roles excluding manager
            permission = ManagerRolePermission()
            permission.has_object_permission(request, self, membership)


        #project id is must becaouse we need to check which project member
        request.data['project_id'] = project_id
        serializer = ProjectMembershipSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user_obj = serializer.validated_data['user']
            send_mail_message(user_obj, project)
            
            serializer.save()
            return Response({'created succefully': serializer.data,'status=':status.HTTP_201_CREATED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, project_id, user):
        if request.user.username == user:
            return Response({f"You can't change your own membership, call the owner"}, status=status.HTTP_404_NOT_FOUND)
        try:
            membership = get_object_or_404(ProjectMembership, user=request.user, project_id=project_id)
        except:
            return Response({f'No membership Found'}, status=status.HTTP_404_NOT_FOUND)
        
        # IsOwnerManagerOrReadOnly include maneger choice manager')           
        permission = IsOwnerManagerOrReadOnly()
        permission.has_object_permission(request, self, membership)

        
        # roles excluding manager
        permission = ManagerRolePermission()
        permission.has_object_permission(request, self, membership)
        
        
        user_membership = get_object_or_404(ProjectMembership, project=project_id, user__username=user)
        print('Cheacking ManagerAccPermission Demotion or Manager Acc')   
        permission = ManagerAccPermission()
        permission.has_object_permission(request, self, user_membership)
        
        request.data['project_id'] = project_id
        request.data['user'] = user
        #ek bar bina user id body me dal ke put karke dekh
        serializer = ProjectMembershipSerializer(user_membership, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'updated account': serializer.data, 'status=': status.HTTP_202_ACCEPTED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Yaha pe mai employeeid le sakta hu it'll be way more easy
    def delete(self, request, project_id, user):
        try:
            membership = get_object_or_404(ProjectMembership, user=request.user, project_id=project_id)
        except:
            return Response({f'No membership Exist with id: {project_id} '}, status=status.HTTP_404_NOT_FOUND)

        print('Cheacking IsOwnerManagerOrReadOnly')   
        permission = IsOwnerManagerOrReadOnly()
        permission.has_object_permission(request, self, membership)


        user_membership = get_object_or_404(ProjectMembership, project=project_id, user__username=user)
        print('Cheacking ManagerAccPermission Demotion or Manager Acc')   
        permission = ManagerAccPermission()
        permission.has_object_permission(request, self, user_membership)

        user_membership.delete()
        return Response({"Removed User": f"{user} is no longer part of this project", "status=": status.HTTP_204_NO_CONTENT})

        
        # return Response({"Removed User": f "{user} is no longer part of this project", "status=": status.HTTP_204_NO_CONTENT})
        # return Response({"Removed User": f"{user} is no longer part of this project", "status=": status.HTTP_204_NO_CONTENT})


# ProjectMembership|ProjectJoinRequest|--DELETE|PUT---DONE2
class JoinAndLeaveProjectAPI(APIView):
    #join
    def post(self, request, project_id):
        try:
            project = get_object_or_404(Project, id=project_id)
        except:
            return Response({'Project': 'Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

        # check if the user already exist
        if ProjectMembership.objects.filter(project_id=project_id, user=request.user).exists():
            return Response(f'You Are Already A Member Of This Project')
        
        if project.is_private:
            # check If Alreay sent the request:
            if ProjectJoinRequest.objects.filter(project_id=project_id, user=request.user).exists():
                return Response(f'You Have Already Sent The Request, Wait For Response', status=status.HTTP_409_CONFLICT)
            ProjectJoinRequest.objects.create(project_id=project_id, user=request.user)
            return Response(f'Sent Request', status=status.HTTP_202_ACCEPTED)

        ProjectMembership.objects.create(project_id=project_id, user=request.user)
        return Response(f'Congrats: Now You are a viewer of {project_id}', status=status.HTTP_201_CREATED)
        # return Response({'Congrats': 'Now You are a viewer of {project_id}', 'account': serializer.data, 'status=': status.HTTP_201_CREATED})
    
    #leave
    def delete(self, request, project_id):
        try:
            project = get_object_or_404(Project, id=project_id)
        except:
            return Response({'Project': 'Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

        # check if the user already exist
        if not ProjectMembership.objects.filter(project_id=project_id, user=request.user).exists():
            return Response(f'You not a  Member Of This Project', status=status.HTTP_403_FORBIDDEN)

        membership = get_object_or_404(ProjectMembership, project_id=project_id, user=request.user)
        membership.delete()
        return Response(f'You are no longer part of {project_id}', status=status.HTTP_204_NO_CONTENT)

    