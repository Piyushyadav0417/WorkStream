from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
    
    def validate(self, data):
        if not data.get('username'):
            raise serializers.ValidationError({'username': 'This field is required.'})
        if not data.get('email'):
            raise serializers.ValidationError({'email': 'This field is required.'})
        if not data.get('password'):
            raise serializers.ValidationError({'password': 'This field is required.'})
        return data


    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_active = False  
        user.save()
        return user
   
    # def validate_password(self, value):
    #     validate_password(value)  # uses Django's built-in validators
    #     return value
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',  'email']
        



    
    
    
    
    
    
    
    
    
# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only = True)
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name',  'password']
        
        
#     def create(self, validated_data):
#         user = User(**validated_data)

#         user.set_password(validated_data['password'])
#         user.save()
#         return user