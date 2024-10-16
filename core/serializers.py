from rest_framework import serializers
from .models import Service, Booking, Rating

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
    '''
class StatSerializer(serializers.Serializer):
    total_bookings = serializers.IntegerField()
    jobs_completed = serializers.IntegerField()
    ratings = serializers.IntegerField()'''