from django.shortcuts import render
from .serializers import ProfileSerializer
from rest_framework.decorators import action
from .models import Profile
from core.models import Booking
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets
# Create your views here.

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action (detail=True, methods=['get'])
    def get_user_stats(self, request, *args, **kwargs):
        user = self.get_object()
        total_booking = Booking.objects.filter(user=user).count()
        return Response({
            'total_booking': total_booking or 0
        })