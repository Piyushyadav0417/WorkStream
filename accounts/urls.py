from django.urls import path
from .views import RegisterAPIView, ProfileAPI, UserProfileAPI, VerifyEmailAPIView, current_user_view
urlpatterns = [
    path('', RegisterAPIView.as_view(), name='register'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('profile/', ProfileAPI.as_view(), name='profile'),
    path('api/me/', current_user_view, name='current_user'),  
]
    # path('auth/', include('accounts.urls')),
