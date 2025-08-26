from django.urls import path
from .views import BoardsAPI, BoardUpdateAPI, TaskListAPI, TaskListUpdateAPI, TaskAPI, TaskAssignmentAPI

from .allviews.project_views import ProjectAPI, ProjectUpdationAPi, TransferProjectOwnershipAPI
urlpatterns = [
# # ProjectUrl
#     # ProjectAPI: GET/POST/PUT/DELETE (100) | DONE2
    path('', ProjectAPI.as_view(), name='project-list-create'), #http://127.0.0.1:8000/api/projects/
    path('<int:project_id>/', ProjectAPI.as_view(), name='project-detail-update-delete'),#http://127.0.0.1:8000/api/projects/project_id/

#     # ProjectUpdationAPi: PUT/DELETE (100) | DONE2
    path('<int:project_id>/edit/', ProjectAPI.as_view(), name='project-update-delete'), #http://127.0.0.1:8000/api/projects/project_id/edit/

#     #TransferProjectOwnershipAPI GET/PUT (Done) | DONE2
    path('<int:project_id>/transferownership/', TransferProjectOwnershipAPI.as_view(), name='project-transferownership'), #http://127.0.0.1:8000/api/projects/<int:project_id>/transferownership/
    path('owners/', TransferProjectOwnershipAPI.as_view(), name='project-owners'), #http://127.0.0.1:8000/api/projects/owners/


# BoardsUrl
    # BoardsAPI: GET/POST (100)
    path('boards/<int:project_id>/', BoardsAPI.as_view(), name='create-all-boards'),#http://127.0.0.1:8000/api/projects/boards/project_id/
    path('board/<int:board_id>/', BoardsAPI.as_view(), name='boards-detail'),#http://127.0.0.1:8000/api/projects/board/board_id/
    # BoardsAPI: UPDATE/DELETE (100)
    path('board/<int:board_id>/update/', BoardUpdateAPI.as_view(), name='boards-update'),#http://127.0.0.1:8000/api/projects/board/board_id/update/
    path('board/<int:board_id>/delete/', BoardUpdateAPI.as_view(), name='boards-delete'),#http://127.0.0.1:8000/api/projects/board/board_id/delete/


#TaskListUrl
    # TaskListAPI: GET/POST (100)
    path('board/task_list/<int:tasklist_id>/', TaskListAPI.as_view(), name='task_list'),#http://127.0.0.1:8000/api/projects/board/task_list/<int:id>/
    path('board/<int:board_id>/task_lists/', TaskListAPI.as_view(), name='board-task_lists'),#http://127.0.0.1:8000/api/projects/board/board_id/tasks/
    # TaskListUpdateAPI: UPDATE/DELETE (100)
    path('task_list/<int:tasklist_id>/update/', TaskListUpdateAPI.as_view(), name='task-update'),#http://127.0.0.1:8000/api/projects/task_list/<int:id>/update/
    path('task_list/<int:tasklist_id>/delete/', TaskListUpdateAPI.as_view(), name='task-delete'),#http://127.0.0.1:8000/api/projects/task_list/<int:id>/update/


#TaskUrl
    # TaskAPI: GET/POST (100)
    path('task/<int:task_id>/', TaskAPI.as_view(), name='task'),#http://127.0.0.1:8000/api/projects/task/<int:id>/
    path('task_list/<int:tasklist_id>/tasks/', TaskAPI.as_view(), name='all-task'),#http://127.0.0.1:8000/api/projects/task_list/<int:task_list_id>/tasks/
    # TaskListUpdateAPI: UPDATE/DELETE (100)
    path('task/<int:task_id>/update/', TaskAPI.as_view(), name='task-update'),#http://127.0.0.1:8000/api/projects/task/<int:task_id>/update/
    path('task/<int:task_id>/delete/', TaskAPI.as_view(), name='task-delete'),#http://127.0.0.1:8000/api/projects/task/<int:task_id>/delete/


# TaskAssignmentUrls
    # TaskAssignmentAPI: GET/POST (100)
    path('task/taskassignment/<int:taskassignment_id>/', TaskAssignmentAPI.as_view(), name='task-taskassignment-detail'),#http://127.0.0.1:8000/api/projects/task/<int:id>/
    path('task/<int:task_id>/taskassignments/', TaskAssignmentAPI.as_view(), name='assign-task'),#http://127.0.0.1:8000/api/projects/task/<int:task_id>/taskassignments/

    # TaskAssignmentAPI: UPDATE/DELETE (100)
    path('task/taskassignment/<int:taskassignment_id>/update/', TaskAssignmentAPI.as_view(), name='task-taskassignment-update'),#http://127.0.0.1:8000/api/projects/task/taskassignment/<int:taskassignment_id>/update/
    path('task/taskassignment/<int:taskassignment_id>/delete/', TaskAssignmentAPI.as_view(), name='task-taskassignment-delete'),#http://127.0.0.1:8000/api/projects/task/taskassignment/<int:taskassignment_id>/delete/


]
    # path('api/projects/', include('projects.urls')),

