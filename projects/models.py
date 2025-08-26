from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

# # done2
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='own_projects')
    project_photo = models.ImageField(upload_to='project_photos/', blank=True, null=True, default='project_photos/default.jpeg')   # Make sure this default file exists
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.owner.username} Created {self.title}"
   
    
class Boards(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='boards')
    title = models.CharField(max_length=255)
    created_by =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards_created')
    file = models.FileField(blank=True, null=True, upload_to='boards_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('project', 'title')

    def __str__(self):
        return f'{self.created_by} → {self.title} → {self.project.title}'


class TaskList(models.Model):
    boards = models.ForeignKey(Boards, on_delete=models.CASCADE, related_name='task_list')
    title = models.CharField(max_length=200)
    position = models.PositiveIntegerField(default=0)
    starting_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} → {self.boards.title}"

class TaskListFiles(models.Model):
    tasklist = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='tasklist_files', blank=True, null=True)

class Task(models.Model):
    STATUS_CHOICE = [
        ('not started', 'Not Started'),
        ('in progress', 'In Progress'),
        ('final touches', 'Final Touches'),
        ('done', 'Done'),
    ]
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')
    ], default='medium')
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default='not started')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @property
    def days_left(self):
        if self.due_date:
            today = timezone.now().date()
            delta = self.due_date - today
            return delta.days
        return None 

class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    assigne_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_time_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('task', 'assigne_to')
        
    def __str__(self):
        return f' assigne  {self.assigne_to} to {self.task.title}'


# ----------------------------------------------------------------------------------
        
# # comments/models.py
# class TaskComment(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
#     content = models.TextField()
#     reply_id = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE)
#     sent_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Comment by {self.user.username} on {self.task.title}"




# # notifications/models.py
# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#     message = models.CharField(max_length=255)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notify: {self.user.username} → {self.message}"


# class ProjectMembership(models.Model):
#     ROLE_CHOICES = [
#         ('manager', 'Manager'),
#         ('member', 'Member'),
#         ('viewer', 'Viewer'),
#     ]

#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')
#     joined_at = models.DateField(auto_now_add=True)

#     class Meta:
#         unique_together = ('project', 'user')

#     def __str__(self):
#         return f"{self.user.username} → {self.project.title} → {self.role}"


# class UserNotification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#     message = models.CharField(max_length=255)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notify: {self.user.username} → {self.message}"
    
    
    
# class ProjectJoinRequest(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='join_requests')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='join_requests')
#     message = models.TextField(blank=True)
#     is_approved = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('project', 'user')

#     def __str__(self):
#         return f"{self.user.username} request to {self.project.title}"
    



# class ProjectNotification(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='notifications')
#     message = models.CharField(max_length=255)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notify: {self.project.title} → {self.message}"