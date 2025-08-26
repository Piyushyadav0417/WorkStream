from django.shortcuts import render, get_object_or_404
from users.models import ProjectMembership
from .models import ProjectJoinRequest
from projects.models import Project, TaskAssignment, Task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import JoinRequestSerializer
from users.permissions import IsOwnerManagerOrReadOnly, ManagerRolePermission, ManagerAccPermission, IsOwnerManager
from rest_framework.pagination import PageNumberPagination
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny
from .token_generator import email_verification_token
from django.core.mail import send_mail

from django.contrib.auth import get_user_model
User = get_user_model()


# ProjectMembership|ProjectJoinRequest|--GET---DONE2
class ProjectJoinRequestsAPI(APIView):
    permission_classes = [IsOwnerManager, permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # filter with username
    def get(self, request, project_id):
        #IsPorject
        try:
            project = get_object_or_404(Project, id=project_id)
        except:
            return Response({'Project': 'Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

        # IsMember
        try:
            #check current user exist in membership
            membership = get_object_or_404(ProjectMembership, user = request.user, project_id=project_id)
        except:
            return Response({'Permission Denied': 'You are not member of this project', 'status=': status.HTTP_403_FORBIDDEN})

        # Get the data
        requests = ProjectJoinRequest.objects.filter(project_id=project_id)
        
        if not project.owner == request.user:
            print('permission is checking')
            self.check_object_permissions(request, membership)

        username = request.query_params.get('user')
        if username:
            requests = requests.filter(user__username__istartswith=username)


        # Pagination
        paginator = PageNumberPagination()
        paginated_projects = paginator.paginate_queryset(requests, request)

        serializer = JoinRequestSerializer(paginated_projects, many=True)
        
        # use paginator's response
        return paginator.get_paginated_response(serializer.data)

        serializer = JoinRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ProjectMembership|ProjectJoinRequest|--DELETE---DONE2
class ProjectJoinRequestAcceptAPI(APIView):
    permission_classes = [IsOwnerManager, permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, project_id, username):
        try:
            project = get_object_or_404(Project, id=project_id)
        except:
            return Response({'Project': 'Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

        # IsMember
        try:
            #check current user exist in membership
            membership = get_object_or_404(ProjectMembership, user = request.user, project_id=project_id)
        except:
            return Response({'Permission Denied': 'You are not member of this project', 'status=': status.HTTP_403_FORBIDDEN})

        
        if not project.owner == request.user:
            self.check_object_permissions(request, membership)
        try:
            request_ = get_object_or_404(ProjectJoinRequest, project_id=project_id, user__username=username)
        except:
            return Response({'Request': 'Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
            
        emp_obj = get_object_or_404(User, username=username)
        ProjectMembership.objects.create(project_id=project_id, user=emp_obj)

        # deleting the request
        request_.delete()
        return Response(f'{username} is now viewer of  {project.title}', status=status.HTTP_201_CREATED)

# ProjectMembership|ProjectJoinRequest|--DELETE---DONE2
class ProjectJoinRequestRejectAPI(APIView):
    # permission_classes = [IsOwnerManager, permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, project_id, username):
        try:
            #check current user exist in membership
            membership = get_object_or_404(ProjectMembership, user = request.user, project_id=project_id)
        except:
            pass
            # return Response({f'You Are  Not Member of this Project'}, status=status.HTTP_403_FORBIDDEN)   
         
        try:
            project = get_object_or_404(Project, id=project_id)
        except:
            return Response({'Project': 'Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # if not project.owner == request.user:
        #     self.check_object_permissions(request, membership)
        try:
            request_ = get_object_or_404(ProjectJoinRequest, project_id=project_id, user__username=username)
        except:
            return Response({'Request': 'Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
            
 
        # deleting the request
        request_.delete()
        return Response(f'{username} Request Rejected From  {project.title}', status=status.HTTP_201_CREATED)

# COMBO OF JOIN&REJECT | DONE2
class ProjectJoinRequestHandleAPI(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerManager]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, project_id, username):
        action = request.data.get('action')
        if action not in ['accept', 'reject']:
            return Response({'detail': "Missing or invalid 'action'. Must be 'accept' or 'reject'."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Get project
        project = get_object_or_404(Project, id=project_id)

        # Check if current user is a member
        membership = ProjectMembership.objects.filter(user=request.user, project=project).first()
        if not membership:
            return Response({'detail': 'You are not a member of this project.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Check permissions
        if project.owner != request.user:
            self.check_object_permissions(request, membership)

        # Get join request
        join_request = get_object_or_404(ProjectJoinRequest, project=project, user__username=username)
        target_user = get_object_or_404(User, username=username)

        # Handle accept or reject
        if action == 'accept':
            ProjectMembership.objects.create(project=project, user=target_user, role='viewer')
            message = f"{username} has been added to project '{project.title}' as a viewer."
        else:  # reject
            message = f"{username}'s join request to project '{project.title}' was rejected."

        join_request.delete()

        return Response({'detail': message}, status=status.HTTP_200_OK)

def send_mail_message(user, *args):
    domain = '127.0.0.1:8000'
    task = None
    assigned_by = None
    project = None

    for arg in args:
        if isinstance(arg, Task):
            task = arg
        elif isinstance(arg, Project):
            project = arg
        elif isinstance(arg, User):
            assigned_by = arg

    if task:
        task_url = reverse('task', kwargs={'task_id': task.id})
        task_link = f"http://{domain}{task_url}"
        subject = f'You’ve been assigned a new task by {assigned_by.username}!'
        message = (
            f"Hello {user.username},\n\n"
            f"{assigned_by.username} has assigned you a new task in the project.\n\n"
            f"🔗 Task Link: {task_link}\n\n"
            "Please click the link to view the task details and begin working on it.\n\n"
            "Best regards,\n"
            "ProjectManager Team"
        )

    elif project:
        print('Yeah Iis calllingkaldnf     ')
        project_url = reverse('project-detail-update-delete', kwargs={'project_id': project.id})
        project_link = f"http://{domain}{project_url}"
        if 'created' in args:
            subject = 'You’ve successfully created a new project!'
            message = (
                f"Hello {user.username},\n\n"
                f"You’ve successfully created a new project titled '{project.title}'.\n\n"
                f"🔗 Project Link: {project_link}\n\n"
                "You can now start adding tasks and invite collaborators.\n\n"
                "Best regards,\n"
                "ProjectManager Team"
            )
        else:
            subject = 'You are now a Project Manager!'
            message = (
                f"Hello {user.username},\n\n"
                "You have been assigned as the **Project Manager** for a new project.\n\n"
                f"🔗 Project Link: {project_link}\n\n"
                "Please click the link to view your project dashboard and begin managing tasks.\n\n"
                "Best regards,\n"
                "ProjectManager Team"
            )

    else:
        # No valid reason for email
        raise ValueError("No task or project provided to send_mail_message.")
    
    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )