from django.contrib import admin
from .models import ProjectMembership, UserNotification
# Register your models here.
admin.site.register(ProjectMembership)
admin.site.register(UserNotification)
