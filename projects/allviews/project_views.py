from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from projects.models import Project
from projects.permissions import IsOwnerOrReadOnly
from projects.serializers import ProjectSerializer, TransferProjectOwnershipSerializer
from notifications.views import send_mail_message

from django.contrib.auth import get_user_model
User = get_user_model()


# views.py

from projects.background_worker import task_queue

class ProjectAPI(APIView):
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, project_id=None):
        if project_id: #getting on project
            try:
                project = get_object_or_404(Project, id=project_id)
                
                # if member:
                #     show details
                # elif private:
                #     show message: This is a private Project
                print(project.is_private)
                serializer = ProjectSerializer(project)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({f'Project with id: {project_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        projects = Project.objects.all()

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 2  # Optional: if you want to override settings.py
        paginated_projects = paginator.paginate_queryset(projects, request)

        serializer = ProjectSerializer(paginated_projects, many=True)
        
        # use paginator's response
        return paginator.get_paginated_response(serializer.data)


    def post(self, request):

        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # This handles validation and error response

        project = serializer.save(owner=request.user)
        send_mail_message(request.user, 'created', project)
        # print('pritig project ownername', project.owner)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProjectAPIBT(APIView):
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, project_id=None):
        # Push to queue instead of processing now
        task_queue.put({
            "action": "GET",
            "request": request,
            "project_id": project_id,
            "data": None
        })

        return Response(
            {"message": "We're working on your project request. Please wait."},
            status=status.HTTP_202_ACCEPTED
        )

    def post(self, request):
        request_data = request.data.copy()

        task_queue.put({
            "action": "POST",
            "request": request,
            "project_id": None,
            "data": request_data
        })

        return Response(
            {"message": "We're creating your project in the background."},
            status=status.HTTP_202_ACCEPTED
        )




class ProjectUpdationAPi(APIView):
    def put(self, request, project_id):
        try:
            project = get_object_or_404(Project, id=project_id)
        except:
            return Response({f'Project with id: {project_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, project)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'updated': serializer.data, 'status=': status.HTTP_202_ACCEPTED})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, project_id):
        try:
            project = get_object_or_404(Project, id=project_id)
        except:
            return Response({f'Project with id: {project_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, project)
        project.delete()
        # return Response({'Delete': 'Project Deleted', 'status=':status.HTTP_204_NO_CONTENT})
        return Response(status=status.HTTP_204_NO_CONTENT)

class TransferProjectOwnershipAPI(APIView):
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, project_id=None):
        print('Its calling')
        if project_id: #getting on project
            try:
                project = get_object_or_404(Project, id=project_id)
                serializer = TransferProjectOwnershipSerializer(project)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Http404:
                return Response({f'Project with id: {project_id} does not exist'}, status=404)
        projects = Project.objects.all()

        # Pagination
        paginator = PageNumberPagination()
        paginated_projects = paginator.paginate_queryset(projects, request)

        serializer = TransferProjectOwnershipSerializer(paginated_projects, many=True)
        
        # use paginator's response
        return paginator.get_paginated_response(serializer.data)

    def put(self, request, project_id):
        if project_id: #getting on project
            try:
                project = get_object_or_404(Project, id=project_id)
            except:
                return Response({f'Project with id: {project_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, project)
        
        data = request.data.copy()
        print('New Owner', data['owner'])
        
        # if not data['owner'] == project.owner.username:
        #     return Response({f'You are already owner2'}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = TransferProjectOwnershipSerializer(project, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'Ownership Transfered': 'You Are No Longer Owner Of this Project', 'new owner': serializer.data, 'status=':status.HTTP_202_ACCEPTED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def projects_views_test(request):

    print('Its working')
    # task = get_object_or_404(Task, id=1)
    # # print(task.title) #Audience Research
    # # print('task board created_by',task.boards.created_by) # user2
    # # print('task board project owner',task.boards.project.owner) # user1

    # # print('project owner: ',task.task_list.boards.project.owner) #project owner user1
    # project = task.task_list.boards.project
    # print('Poject owner', project.owner)
    # print('Poject id', project.id)
    # print('Secco proj owner', project.members.all())
    # members = task.task_list.boards.project.members.all()
    # if request.user in members:
    #     print('Yeah hes members ')
    # print('working with', request.user)
    # # user1 is owner and user2 is manager
    # print('all members from of the project',task.task_list.boards.project.members.all()) #get all project members
    # # request.user in task.task_list.boards.project.members.all()
    # # board = get_object_or_404(Boards, id=1)
    # # print('board creater',board.created_by)
    # # print('board project owner',board.project.owner)
    # # project = get_object_or_404(Project, id=1)
    # # print('project owner', project.owner)
    # print('project boards creater',project.boards.created_by)
    return render(request, 'projects/projects_temp.html')


# class ProjectAPI(APIView):
#     permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    
#     def get(self, request, project_id=None):
#         if project_id: #getting on project
#             try:
#                 project = get_object_or_404(Project, id=project_id)
                
#                 # if member:
#                 #     show details
#                 # elif private:
#                 #     show message: This is a private Project
#                 print(project.is_private)
#                 serializer = ProjectSerializer(project)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except:
#                 return Response({f'Project with id: {project_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)


#         projects = Project.objects.all()

#         # Pagination
#         paginator = PageNumberPagination()
#         paginator.page_size = 2  # Optional: if you want to override settings.py
#         paginated_projects = paginator.paginate_queryset(projects, request)

#         serializer = ProjectSerializer(paginated_projects, many=True)
        
#         # use paginator's response
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request):

#         serializer = ProjectSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)  # This handles validation and error response

#         project = serializer.save(owner=request.user)
#         send_mail_message(request.user, 'created', project)
#         # print('pritig project ownername', project.owner)
        
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
