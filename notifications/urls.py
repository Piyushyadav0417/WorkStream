from django.urls import path
from .views import ProjectJoinRequestsAPI, ProjectJoinRequestAcceptAPI, ProjectJoinRequestRejectAPI, ProjectJoinRequestHandleAPI
urlpatterns = [
    path('project/joinrequests/<int:project_id>/', ProjectJoinRequestsAPI.as_view(), name='project-join-requests'), #http://127.0.0.1:8000/api/notifications/project/joinrequests/<int:project_id>/
    path('project/<int:project_id>/accept-join-request/<str:username>/', ProjectJoinRequestAcceptAPI.as_view(), name='project-accept-join-requests'), #http://127.0.0.1:8000/api/notifications/project/<int:project_id>/accept-join-request/<str:username>/
    path('project/<int:project_id>/reject-join-request/<str:username>/', ProjectJoinRequestRejectAPI.as_view(), name='project-accept-join-requests'), #http://127.0.0.1:8000/api/notifications/project/<int:project_id>/accept-join-request/<str:username>/
    path('project/<int:project_id>/join-request-handle/<str:username>/', ProjectJoinRequestHandleAPI.as_view(), name='project-accept-join-requests'), #http://127.0.0.1:8000/api/notifications/project/<int:project_id>/accept-join-request/<str:username>/

]
    # path('api/notifications/', include('notifications.urls')),
