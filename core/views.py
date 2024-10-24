from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Service, Booking
from users.models import Profile
from .serializers import ServiceSerializer, BookingSerializer
from django.core.mail import send_mail

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.filter(user=user).first()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save(profile=profile)

        # Send the confirmation email using Brevo SMTP
        subject = 'Booking Confirmation'
        message = f"Hello {user.first_name},\n\nYour booking is confirmed for {booking.date} at {booking.time}."
        recipient_email = user.email

        send_mail(
            subject,
            message,
            'abdulhamidusman218@gmail.com',
            ['nothamido3@gmail.com'],         # To email
            fail_silently=False,
        )
        return Response('booking was successful! You should receive an email soon', status=status.HTTP_201_CREATED)

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(f'Deleted booking of {instance.service}')