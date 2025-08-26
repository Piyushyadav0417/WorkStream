from rest_framework import serializers
from .models import ProjectJoinRequest
from django.contrib.auth import get_user_model
from projects.models import Project
User = get_user_model()


class JoinRequestSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    project = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Project.objects.all()
    )
    class Meta:
        model = ProjectJoinRequest
        fields = '__all__'
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Dynamically make all fields read-only
#         for field in self.fields.values():
#             field.read_only = True




# #show all members : current we are working on this 
# #show members seprately for this project (manager profile in X Project. Owner Profile In X group, all) : projectid/memberdetails/memberid