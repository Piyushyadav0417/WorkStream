from django.contrib import admin
from .models import Project, Task, TaskAssignment, TaskList, Boards, TaskListFiles
# Register your models here.
admin.site.register(Project)
admin.site.register(Boards)
admin.site.register(Task)
admin.site.register(TaskAssignment)
admin.site.register(TaskList)
admin.site.register(TaskListFiles)