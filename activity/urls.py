from django.urls import path
from .views import activity_test
urlpatterns = [
    path('', activity_test, name='activity_test'),
]