from rest_framework import serializers
from .models import Project, Boards, TaskList, Task, TaskAssignment, TaskListFiles
from django.contrib.auth import get_user_model
User = get_user_model()

# HERE'S SOME STRICT RULES IN IT
class StrictModelSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        # fields that are defined in the serializer
        all_fields = self.fields

        # fields that are writeable (not read-only)
        writable_fields = {
            name for name, field in all_fields.items() if not field.read_only
        }

        # anything that was sent but is not writeable = should be blocked
        unknown_or_readonly = set(data.keys()) - writable_fields

        if unknown_or_readonly:
            raise serializers.ValidationError({
                field: "This field is not allowed (unknown or read-only)." 
                for field in unknown_or_readonly
            })

        return super().to_internal_value(data)

# ----------------------------------------------------------------------------------------------------
# Project | DONE2
class TransferProjectOwnershipSerializer(StrictModelSerializer):
    owner = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Project
        fields = ['id', 'title', 'owner']

    def validate(self, data):
        if data['owner'] == self.context['request'].user:
            raise serializers.ValidationError("You are already the owner.")
        return data

# ----------------------------------------------------------------------------------------------------
# Project | DONE2
class ProjectSerializer(StrictModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'owner']

    def validate_project_photo(self, value):
        max_size = 5 * 1024  # 5MB in bytes
        if value and value.size > max_size:
            raise serializers.ValidationError("Image size should not exceed 5KB.")
        return value
        
        # owner = request.user we can also do here, right? but even what is the best practice serializers or views

# ----------------------------------------------------------------------------------------------------
        
class TaskAssignmentSerializer(serializers.ModelSerializer):
    
    task = serializers.SerializerMethodField()
    task_id = serializers.PrimaryKeyRelatedField(
        queryset = Task.objects.all(),
        source = 'task',
        required = False
    )
    # read_only	False | required	True
    assigne_to = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        slug_field='username',
        required =False
    )
    
    class Meta:
        model = TaskAssignment
        fields = ['id', 'task_id', 'task', 'assigne_to', 'assigned_at', 'assigned_time_updated_at']
        read_only_fields = ['id',  'task',  'assigned_at', 'assigned_time_updated_at']

    def get_task(self, obj):
        return obj.task.title

# ---------------------------------------------------------------------------------
class TaskSerializer(serializers.ModelSerializer):
    task_list = serializers.SerializerMethodField()
    task_list_id = serializers.PrimaryKeyRelatedField(
        queryset = TaskList.objects.all(),
        source = 'task_list'
    )
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Task
        # here's assign user can update - status only
        fields = ['id', 'task_list_id', 'task_list', 'title', 'description', 'due_date', 'priority', 'status', 'created_by', 'created_at', 'days_left']
        read_only_fields = ['id', 'task_list_id', 'task_list', 'due_date', 'priority',  'created_by', 'created_at', 'days_left']

    def get_task_list(self, obj):
        return obj.task_list.title
# ----------------------------------------------------------------------------------------------------

class BoardsSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    project_id = serializers.PrimaryKeyRelatedField(
        queryset = Project.objects.all(),
        source = 'project'
    )
    
    created_by = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        slug_field = 'username',
        required =False
        ) 

    class Meta:
        model = Boards
        fields = ['id', 'project', 'project_id', 'title', 'created_by', 'created_at', 'updated_at', 'file']
        read_only_fields = ['id', 'project', 'project_id', 'created_by', 'created_at', 'updated_at']
        
    def get_project(self, obj):
        return obj.project.title
# ----------------------------------------------------------------------------------------------------
    # path('board/task_list/<int:tasklist_id>/', TaskListAPI.as_view(), name='task_list'),#http://127.0.0.1:8000/api/projects/board/task_list/<int:tasklist_id>/
    # path('board/<int:board_id>/task_lists/', TaskListAPI.as_view(), name='board-task_lists'),#http://127.0.0.1:8000/api/projects/board/board_id/tasks/
    # # TaskListUpdateAPI: UPDATE/DELETE (100)
    # path('task_list/<int:tasklist_id>/update/', TaskListUpdateAPI.as_view(), name='task-update'),#http://127.0.0.1:8000/api/projects/task_list/<int:id>/update/
    # path('task_list/<int:tasklist_id>/delete/', TaskListUpdateAPI.as_view(), name='task-delete'),#http://127.0.0.1:8000/api/projects/task_list/<int:id>/update/

class TaskListFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskListFiles
        fields = ['file']

class TaskListSerializer(serializers.ModelSerializer):
    files = TaskListFilesSerializer(many=True, read_only=True)  # ✅ FIXED
    board_id = serializers.PrimaryKeyRelatedField(
        queryset=Boards.objects.all(),
        source='boards',
        required=False,
    )
    boards = serializers.SerializerMethodField()

    class Meta:
        model = TaskList
        fields = ['id', 'title', 'board_id', 'boards', 'position', 'files', 'starting_date']
        read_only_fields = ['id', 'boards', 'board_id', 'starting_date']

    def get_boards(self, obj):
        return obj.boards.title

# here what I understood:
# project_id = serializers.PrimaryKeyRelatedField(
#     queryset=Project.objects.all(),
#     source='project'
# )
# it just says in the current model, or the serializer we are working on add a filed that from the orignal poroject field, use it as project_id (project object id)

# now for SlugRelatedField
# created_by = serializers.SlugRelatedField(
#     queryset=User.objects.all(),
#     slug_field='username'
# )
# there is a filed name created_by present it username. (because it's fk from User model we took all the user's from User model and use thier username to show/write)

# Now for SerializerMethodField
#     project = serializers.SerializerMethodField()
# there is a field called project, we are going to customize it(for how to use and show it).
# then we do:
#     def get_project(self, obj):
#         return obj.project.title
# it says for the current object there is a fk called project use that project title, it's read_only field