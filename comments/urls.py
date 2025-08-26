from django.urls import path
from .views import com
urlpatterns = [
    path('', com, name='comments_temp'),

]