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
                'firstname', 'lastname', 'user', 'phone_number',
                'state', 'region', 'address',
                'avatar', 'created_at', 'user'
                ]
        read_only_fields = ['created_at', 'user']