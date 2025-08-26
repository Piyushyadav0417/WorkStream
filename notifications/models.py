from django.db import models
from projects.models import Project
from django.contrib.auth import get_user_model
User = get_user_model()
# # Create your models here.

# # notifications/models.py

# DONE2 | SERIALIZER | API | PERMISSIONS|
class ProjectJoinRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='join_requests')
    message = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user.username} request to {self.project.title}"
    



# #Notification wala kamm baad me
# # notifications/models.py : Personal Notification

    
# # notifications/models.py : Project Notification
class ProjectNotification(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notify: {self.project.title} → {self.message}"

