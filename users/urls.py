from django.urls import path
from .views import users_temp, ProjectMembershipAPI, JoinAndLeaveProjectAPI
urlpatterns = [
    # ProjectMembershipAPI|DONE2
    path('project/<int:project_id>/', ProjectMembershipAPI.as_view(), name='project-membership-get-post'), #http://127.0.0.1:8000/api/users/project/<int:project_id>/
    path('project/<int:project_id>/user/<str:user>/', ProjectMembershipAPI.as_view(), name='project-membership-put-delete'), #http://127.0.0.1:8000/api/users/project/<int:project_id>/user/str:user/

    
    # JoinAndLeaveProjectAPI -|POST|DELETE|- DONE2
    path('join/project/<int:project_id>/', JoinAndLeaveProjectAPI.as_view(), name='project-join'), #http://127.0.0.1:8000/api/users/join/project/<int:project_id>/
    # path('leave/project/<int:project_id>/', JoinAndLeaveProjectAPI.as_view(), name='project-leave'), #http://127.0.0.1:8000/api/users/leave/project/<int:project_id>/




    
]

    # path('api/users/', include('users.urls')),
