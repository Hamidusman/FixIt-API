from rest_framework import serializers
from .models import Service, Booking, Rating
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class StatSerializer(serializers.Serializers):
    total_bookings = serializers.IntegerField()
    jobs_completed = serializers.IntegerField()
    ratings = serializers.IntegerField()