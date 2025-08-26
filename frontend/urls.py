from django.urls import path
from . import views

# urlpatterns = [
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('', views.project_list, name='project_list'),
#     path('create/', views.project_create, name='project_create'),
#     path('update/<int:project_id>/', views.project_update, name='project_update'),
#     path('delete/<int:project_id>/', views.project_delete, name='project_delete'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.project_create, name='project_create'),  # 👈 Add this
    path('update/<int:project_id>/', views.project_update, name='project_update'),
    path('delete/<int:project_id>/', views.project_delete, name='project_delete'),

]
