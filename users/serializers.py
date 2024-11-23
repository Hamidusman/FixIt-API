from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User, Profile

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
                'id', 'firstname', 'lastname', 'phone_number',
                'state', 'region', 'address',
                'avatar', 'created_at', 'user'
                ]
        read_only_fields = ['id', 'created_at', 'user']
        
class UserSerializer(serializers.ModelSerializer):
    
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'profile']