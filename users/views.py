from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .serializers import ProfileSerializer
from rest_framework.decorators import action
from .models import Profile
from core.models import Booking
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from djoser.views import UserViewSet
# Create your views here.

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        user = request.user

        # Check if profile for the user already exists
        if Profile.objects.filter(user=user).exists():
            return Response(
                {"detail": "You already created a profile!"},
                status=400
            )
        
        # Create the profile with user automatically assigned
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save the profile with the current authenticated user
        serializer.save(user=user)
        
        return Response(serializer.data, status=201)


'''    @action (detail=True, methods=['get'])
    def get_user_stats(self, request, *args, **kwargs):
        user = self.get_object()
        total_booking = Booking.objects.filter(user=user).count()
        return Response({
            'total_booking': total_booking or 0
        })
        '''
'''class CustomUserViewSet(UserViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "id"
    
    
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated]
    )
    def dashboard(self, request, *args, **kwargs):
        profile = request.user.profile
        total_booking = Booking.objects.filter(profile=profile)
    '''