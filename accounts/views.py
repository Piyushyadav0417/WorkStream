from django.shortcuts import render
from .serializers import UserRegistrationSerializer, ProfileSerializer, UserRegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .token_generator import email_verification_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


User = get_user_model()
# Create your views here.

            # print('uidb64',uidb64) #p2,14:MTQ | p2,15:MTU | p2,16:MTY |  p2,17:MTc | p3,18:MTg 
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print('request', request)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print('user', user)

            # Generate UID and token
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk)) # DATA-->BYTES-->ENCODE(ASCII FORMATE). | MjA
            print('uidb64:', uidb64)
            token = email_verification_token.make_token(user) #IT'S CREATE A TOKEN FOR THE ENCODED DATA
            print(f'type:{type(token)}token: {token}')
            # Build activation URL
            domain = get_current_site(request).domain #127.0.0.1:8000

            
            verify_url = reverse('verify-email', kwargs={'uidb64': uidb64, 'token': token})# /auth/verify-email/MjA/cp8kvz-9489e6b385a71b35abd6114d7bd3854b/
            print('verify_url:', verify_url)
            activation_link = f"http://{domain}{verify_url}"
            print('activation_link:', activation_link)
            # Send email
            subject = 'Verify your email for Project Manager'
            message = f'Hi {user.username},\n\nPlease verify your email by clicking the link below:\n{activation_link}\n\nThank you!'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return Response({'message': 'User registered. Check your email to verify your account.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        

class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, uidb64, token):
        try:
            # Decode UID
            uid = force_str(urlsafe_base64_decode(uidb64))
            # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            

            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({'error': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({'message': 'Account already verified.'}, status=status.HTTP_200_OK)

        if email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully. You can now log in.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPI(APIView):
    
    
    def get(self, request):
        return Response({
            'user_name': request.user.username,
            'first_name': request.user.first_name
        })
        
class UserProfileAPI(APIView):
    def put(self, request):
        profile = User.objects.get(username=request.user.username)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # This will call the 'create' method and hash the password
            return Response({'message': 'User Profile updated successfully', 'Updated Profile': serializer.data}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })