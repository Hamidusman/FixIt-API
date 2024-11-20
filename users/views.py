from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .serializers import ProfileSerializer, UserSerializer
from rest_framework.decorators import action
from .models import Profile, User
from core.models import Booking
from core.serializers import BookingSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet
# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        if Profile.objects.filter(user=user).exists():
            return Response(
                {"detail": "You already created a profile!"},
                status=400
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save(user=user)
        
        return Response(serializer.data, status=201)

    def patch(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        if profile is None:
            return Response({'Error: Profile does not exist'},status=404)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action (detail=False, methods=['get'], url_path='me')
    def my_profile(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        if profile is None:
            return Response({'Error: Profile does not exist'},status=404)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action (detail=False, methods=['get'], url_path='user-stat')
    def get_user_stats(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        total_booking = Booking.objects.filter(profile=profile).count()
        completed = Booking.objects.filter(profile=profile, status='completed').count()
        #pending = Booking.objects.filter(profile=profile, status='pending').count()
        
        return Response({
            'total_booking': total_booking,
            'completed': completed,
        })

    @action(
        detail=False,methods=["get"],
        permission_classes=[IsAuthenticated]
    )
    def user_booking_log(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        bookings = Booking.objects.filter(profile=profile)
        
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


'''class CustomUserViewSet(UserViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "id"
    
    
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated]
    )
    '''