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
        profile, created = Profile.objects.get_or_create(user=user)
        if not created:
            return Response(
                {"detail": "You already created a profile!"},
                status=400
            )
        serializer = self.get_serializer(instance=profile, data=request.data)
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
    
    @action (detail=False, methods=['get'], url_path='user-stat')
    def get_user_stats(self, request, *args, **kwargs):
        user = request.user
        profile = self.get_profile(user)

        stats = Booking.objects.filter(profile=profile).values('profile').annotate(
            total_booking=Count('id'),
            completed_booking=Count('id', filter=Q(status='completed'))
        ).first()

        if stats is None:
            stats = {'total_booking': 0, 'completed_booking': 0}

        return Response({
            'total_booking': stats.get('total_booking', 0),
            'completed': stats.get('completed_booking', 0)
        })

    @action(
        detail=False,methods=["get"],
        permission_classes=[IsAuthenticated]
    )
    def user_booking_log(self, request, *args, **kwargs):
        user = request.user
        bookings = Booking.objects.filter(profile__user=user).select_related('profile')
        
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