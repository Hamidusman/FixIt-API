from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.cache import cache

from .models import Rating, Booking
from users.models import Profile
from .serializers import RatingSerializer, BookingSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail

#from Fixit_API.tasks import send_booking_email




class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('profile')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        '''
        subject = 'Booking Confirmation'
        message = f"Dear {profile.firstname},\n\nYour booking has been successfully confirmed."
        recipient_list = [profile.user.email]
        send_booking_email.delay(subject, message, recipient_list)'''
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(f'Deleted booking for {instance.service}')
class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(reviewer=self.request.user)

    def perform_create(self, serializer):
        booking = serializer.validated_data.get('booking')
        self.validate_booking(booking)
        serializer.save(reviewer=self.request.user)
        
    def validate_booking(self, booking):
        if booking.profile.user != self.request.user:
            return(ValidationError, "You can only rate your own booking")
        if booking.status != 'completed':
            return(ValidationError, 'Can only rate completed services')