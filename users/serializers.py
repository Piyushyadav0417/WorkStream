from rest_framework import serializers
from .models import ProjectMembership, UserNotification
# from notifications.models import ProjectJoinRequest 
from django.contrib.auth import get_user_model
from projects.models import Project
User = get_user_model()

# done2
class ProjectMembershipSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    ) 
    
        
    project = serializers.SerializerMethodField(read_only=True)
    
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),   # ⚡ Adding new field project id withh projeect
        source='project'
    )
    
    class Meta:
        model = ProjectMembership
        fields = ['id', 'project', 'project_id', 'user', 'role', 'joined_at']
        read_only_fields = ['id', 'joined_at', 'project', 'project_id']

    def get_project(self, obj):
        return obj.project.title
    
    def validate(self, data):
        request = self.context.get('request')

        if request and request.method == 'POST':
            if not data['user']:
                raise serializers.ValidationError("this field is required")
        return data

    
# ---------------------------------------------
# done2
class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ['message', 'created_at', 'is_read']
        read_only_fields = ['message', 'created_at']
        
        
# class JoinRequestSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(
#         slug_field='username',
#         queryset=User.objects.all()
#     )
#     project = serializers.SlugRelatedField(
#         slug_field='title',
#         queryset=Project.objects.all()
#     )
#     class Meta:
#         model = ProjectJoinRequest
#         fields = '__all__'
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Dynamically make all fields read-only
#         for field in self.fields.values():
#             field.read_only = True




# #show all members : current we are working on this 
# #show members seprately for this project (manager profile in X Project. Owner Profile In X group, all) : projectid/memberdetails/memberid