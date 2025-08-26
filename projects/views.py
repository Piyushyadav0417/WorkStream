#Transer OwnerShip-----TransferOwnerShipOfProjectAPI---------------only owner can acces this api---proeject_id/transerownership/emp_id/ : emp_id should be the manager
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Project, Boards, TaskList, Task, TaskAssignment
from users.models import ProjectMembership
from .serializers import ProjectSerializer, BoardsSerializer, TaskListSerializer, TaskSerializer, TaskAssignmentSerializer
from .permissions import IsCreaterOwnerOrReadOnly, IsBoardsOwnerProjectOwnerOrReadOnly, IsOwnerCreatorAssigneeOrReadOnly, IsOwnerTaskCreatorOrReadOnly
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from users.permissions import IsOwnerManagerOrReadOnly
from notifications.views import send_mail_message
from django.contrib.auth import get_user_model
User = get_user_model()

#Done 
class BoardsAPI(APIView):
    permission_classes = [IsOwnerManagerOrReadOnly, permissions.IsAuthenticated]
    def get(self, request, project_id=None, board_id=None):
        
        if board_id:
            # Fetch single board
            board = get_object_or_404(Boards, id=board_id, project_id=project_id)
            serializer = BoardsSerializer(board)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        try:
            project = get_object_or_404(Project, id=project_id)
        except:
            return Response({f'Project with id: {project_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        if project.is_private:
            if not project.owner == request.user or not project.memberships.filter(user=request.user).exists():
                return Response('T')


        #Get all boards from project id
        boards = Boards.objects.filter(project_id=project_id)
        
        # if not boards:
        #     print('None Boards------------------------------------------------------------------------------------------')
        # Fetch list of boards
        creator = request.query_params.get('creator_id')
        if creator:
            boards = boards.filter(created_by__username__icontains=creator)

        # Pagination
        paginator = PageNumberPagination()
        paginated_projects = paginator.paginate_queryset(boards, request)

        serializer = BoardsSerializer(paginated_projects, many=True)
        
        # use paginator's response
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, project_id):
        print("CallingGG")
        # Check if project exists
        try:
            project= get_object_or_404(Project, id=project_id)
        except:
            return Response({"Project Not Exist": "Please Enter The RIght Project ID", "status=":status.HTTP_404_NOT_FOUND})

        if not project.owner == request.user:
            membership = get_object_or_404(ProjectMembership, user=request.user, project_id=project_id)
            self.check_object_permissions(request, membership)

        # Attach project_id and created_by to incoming data
        data = request.data.copy()
        data['project_id'] = project_id

        serializer = BoardsSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # -----------------------------------------------------------------------------
# Done 
class BoardUpdateAPI(APIView):
    permission_classes = [IsCreaterOwnerOrReadOnly, permissions.IsAuthenticated]
    def put(self, request, board_id):
        try:
            board = get_object_or_404(Boards, id=board_id)
        except:
            return Response({'Not Found': 'This Board Does Not Exist', 'status=':status.HTTP_404_NOT_FOUND})
        
        if not board.created_by == request.user:
            self.check_object_permissions(request, board)
        serializer = BoardsSerializer(board, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, board_id):
        board = get_object_or_404(Boards, id=board_id)
        if not board.created_by == request.user:
            self.check_object_permissions(request, board)
        board.delete()
        return Response({"message": "Board deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# # ----------------------------------------------------------------------------
#Done
class TaskListAPI(APIView):
    def get(self, request, board_id=None, tasklist_id=None):
        if tasklist_id:
            try:
                task = get_object_or_404(TaskList, id=tasklist_id)
                print(task)
                serializer = TaskListSerializer(task)
                return Response({"Task": serializer.data, "status=":status.HTTP_200_OK})
            except:
                return Response({"Task Not Present": "Please Enter valid task id", "status=":status.HTTP_404_NOT_FOUND})
        if board_id:
            try:
                board = get_object_or_404(Boards, id=board_id)
            except:
                return Response({"Board Not Present": "Please Enter valid task id", "status=":status.HTTP_404_NOT_FOUND})
            board_tasks = TaskList.objects.filter(boards=board_id)
            serializer = TaskListSerializer(board_tasks, many=True)
            return Response({"Board Tasks": serializer.data, "status=":status.HTTP_200_OK})
            
    def post(self, request, board_id):
        try:
            board = get_object_or_404(Boards, id=board_id)
        except:
            return Response(
                {"error": "Board not found. Please provide a valid board ID."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(boards=board)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------------------------
#Done 100
class TaskListUpdateAPI(APIView):
    permission_classes = [IsBoardsOwnerProjectOwnerOrReadOnly, permissions.IsAuthenticated]
    def put(self, request, tasklist_id):
        try:
            task = get_object_or_404(TaskList, id=tasklist_id)
        except:
            return Response({"Task Not Present": "Please Enter valid task id", "status=":status.HTTP_404_NOT_FOUND})
        
        if not task.boards.created_by == request.user:
            self.check_object_permissions(request, task)
        serializer = TaskListSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Updated': "Object", 'status=': status.HTTP_202_ACCEPTED})
        return Response({"Erros Accured": serializer.errors, "status=":status.HTTP_400_BAD_REQUEST})
            
    def delete(self, request, tasklist_id):
        try:
            task = get_object_or_404(TaskList, id=tasklist_id)
        except:
            return Response({"Task Not Present": "Please Enter valid task id", "status=":status.HTTP_404_NOT_FOUND})

        if not task.boards.created_by == request.user:
            self.check_object_permissions(request, task)
        
        task.delete()
        return Response({"message": "Board deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            
# ----------------------------------------------------------------------------
#Done 100 
class TaskAPI(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, tasklist_id=None, task_id=None):
        if id:
            try:
                task = get_object_or_404(Task, id=task_id)
                print(task)
                serializer = TaskSerializer(task)
                return Response({"Task": serializer.data, "status=":status.HTTP_200_OK})
            except:
                return Response({"Task Not Present": "Please Enter valid task id", "status=":status.HTTP_404_NOT_FOUND})
        if tasklist_id:
            try:
                task_list = get_object_or_404(TaskList, id=tasklist_id)
            except:
                return Response({"TaskList Not Present": "Please Enter valid TaskList id", "status=":status.HTTP_404_NOT_FOUND})

            task_list = Task.objects.filter(task_list=tasklist_id)

            # Pagination
            paginator = PageNumberPagination()
            paginated_task_list = paginator.paginate_queryset(task_list, request)

            serializer = TaskSerializer(paginated_task_list, many=True)
            
            # use paginator's response
            return paginator.get_paginated_response(serializer.data)


    def post(self, request, tasklist_id):
        try:
            task_list = get_object_or_404(TaskList, id=tasklist_id)
        except:
            return Response({"Task Not Present": "Please Enter valid Task id", "status=":status.HTTP_404_NOT_FOUND})
        
        # check permissions
        board = task_list.boards
        permission = IsBoardsOwnerProjectOwnerOrReadOnly()
        permission.has_object_permission(request, self, board)
        data = request.data.copy()
        data['task_list_id'] = tasklist_id
        # print(board_id)
        serializer = TaskListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
        except:
            return Response({"Task Not Present": "Please Enter valid task id", "status=":status.HTTP_404_NOT_FOUND})
        
        if not task.created_by == request.user:
            permission = IsOwnerCreatorAssigneeOrReadOnly()
            permission.has_object_permission(request, self, task)

        updating_fields = set(request.data.keys())        
        restricted_fields = {'title', 'description', 'priority'}

        if restricted_fields.intersection(updating_fields):
            # Assinee Only Update Status
            permission = IsOwnerTaskCreatorOrReadOnly()
            permission.has_object_permission(request, self, task)

        if not task.created_by == request.user:
            self.check_object_permissions(request, task)
        
        # return task.created_by == request.user or task.task_list.boards.project.owner == request.user
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Updated task': serializer.data, 'status=': status.HTTP_202_ACCEPTED})
        return Response({"Erros Accured": serializer.errors, "status=":status.HTTP_400_BAD_REQUEST})
   
    def delete(self, request, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
        except:
            return Response({"Task Not Present": "Please Enter valid task id", "status=":status.HTTP_404_NOT_FOUND})
        
        if not task.created_by == request.user:
            permission = IsOwnerTaskCreatorOrReadOnly()
            permission.has_object_permission(request, self, task)
            
        task.delete()
        return Response({"message": "task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------------------------------
class TaskAssignmentAPI(APIView):
    permission_classes = [IsOwnerTaskCreatorOrReadOnly, permissions.IsAuthenticated]
                                                                                                                      
    def get(self, request, taskassignment_id=None, task_id=None):
        if taskassignment_id: #getting on taskassignment
            try:
                taskassignment = get_object_or_404(TaskAssignment, id=taskassignment_id)
                serializer = TaskAssignmentSerializer(taskassignment)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({f'{taskassignment} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # check task exist
        try:
            task = get_object_or_404(Task, id=task_id)
        except:
            return Response({f'{task_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    
        taskassignments = TaskAssignment.objects.filter(task=task_id)
        # Pagination
        paginator = PageNumberPagination()
        taskassignments = paginator.paginate_queryset(taskassignments, request)

        serializer = TaskAssignmentSerializer(taskassignments, many=True)
        # use paginator's response
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
            #only task creater|projectowner permission
        except:
            return Response({f'Not Task Exist with {task_id}'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, task)
        # data = request.data.copy()
        # data['project_id'] = project_id

        # serializer = BoardsSerializer(data=data)
        data = request.data.copy()
        data['task_id'] = task_id
        # data_copy
        serializer = TaskAssignmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            assigne_to = serializer.validated_data['assigne_to']
            send_mail_message(assigne_to, request.user, task)
            return Response({'taskassigned': serializer.data, 'status=':status.HTTP_201_CREATED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    def put(self, request, taskassignment_id):
        try:
            taskassignment = get_object_or_404(TaskAssignment, id=taskassignment_id)
        except:
            return Response({f'{taskassignment} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        task = taskassignment.task
        self.check_object_permissions(request, task)
        
        serializer = ProjectSerializer(taskassignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'updated': serializer.data, 'status=':status.HTTP_202_ACCEPTED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, taskassignment_id):
        try:
            taskassignment = get_object_or_404(TaskAssignment, id=taskassignment_id)
        except:
            return Response({f'{taskassignment} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        task = taskassignment.task
        self.check_object_permissions(request, task)
        
        taskassignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)