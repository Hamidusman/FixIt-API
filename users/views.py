from django.shortcuts import render
from .serializers import ProfileSerializer
from .models import Profile
from rest_framework.views import APIView
from rest_framework import generics
# Create your views here.

class CreateProfile(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

