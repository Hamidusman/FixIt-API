from rest_framework import viewsets, status
from django.conf import settings
from rest_framework.response import Response
from .models import Rating, Booking
from users.models import Profile
from .serializers import RatingSerializer, BookingSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail

from ..Fixit_API.tasks import send_booking_email



class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.filter(user=user).first()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(profile=profile)
        '''     
        subject = 'Booking Confirmation'
        message = f"Dear {profile.firstname},\n\nYour booking has been successfully confirmed."
        recipient_list = [profile.user.email]
        send_booking_email.delay(subject, message, recipient_list)
        '''
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(f'Deleted booking for {instance.service}')

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        return Rating.objects.filter(booking__profile__user=self.request.user)

    def perform_create(self, serializer):
        booking = serializer.validated_data.get('booking')
        if booking.profile.user != self.request.user:
            raise ValidationError("You can only rate your own bookings.")

        # makes sure booking is completed before allowing a rating
        if booking.status != 'completed':
            raise ValidationError("You can only rate completed bookings.")

        serializer.save(reviewer=self.request.user)