from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from django.db.models import Count, Q
from rest_framework.decorators import action
from .models import Profile
from core.models import Booking
from core.serializers import BookingSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.shortcuts import get_object_or_404
# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_profile(self, user):
        return get_object_or_404(Profile.objects.select_related('user'), user=user)
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=201)

    def patch(self, request, *args, **kwargs):
        user = request.user
        profile = self.get_profile(user)
        
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action (detail=False, methods=['get'], url_path='me')
    def my_profile(self, request, *args, **kwargs):
        user = request.user
        profile = self.get_profile(user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'], url_path='user-stat')
    def get_user_stats(self, request, *args, **kwargs):
        user = request.user
        total_booking = Booking.objects.filter(user=user).count()
        completed = Booking.objects.filter(user=user, status='completed').count()
        return Response({
            'total_booking': total_booking,
            'completed': completed})

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def user_booking_log(self, request, *args, **kwargs):
        user = request.user
        logs = Booking.objects.select_related('user').filter(user=user).order_by('-date')

        serializer = BookingSerializer(logs, many=True)
        print("Serialized data:", serializer.data)
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