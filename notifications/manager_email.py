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

User = get_user_model()