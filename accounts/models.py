from django.contrib.auth.models import AbstractUser
from django.db import models

# class CustomUser(AbstractUser):
#     GENDER_CHOICE = [
#         ('male', 'Male'),
#         ('female', 'Female')
#     ]
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     gender = models.CharField(choices=GENDER_CHOICE, blank=True, null=True, max_length=20)
#     profile = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/male.jpeg')


#     def __str__(self):
#         return self.username
    
#     class Meta:
#         swappable = 'AUTH_USER_MODEL'