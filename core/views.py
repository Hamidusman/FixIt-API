from rest_framework import viewsets, status
from django.conf import settings
from rest_framework.response import Response
from .models import Rating, Booking
from users.models import Profile
from .serializers import RatingSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail



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
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['abdulhamidusman218@gmail.com']
        send_mail(subject, message, from_email, recipient_list)
        '''
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(f'Deleted booking for {instance.service}')

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = [IsAuthenticated]
    

    