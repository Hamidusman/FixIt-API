from rest_framework import serializers
from .models import Service, Booking, Rating
from users.models import Profile

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'profile', 'service', 'phone_number', 'description',
                  'region', 'address', 'state',
                  'date', 'time', 'duration',
                  'created_at', 'status'
                  ]
        read_only_fields = ['profile', 'created_at']

    def validate_status(self, value):
        if value not in dict(Booking.STATUS_CHOICES):
            return serializers.ValidationError('Invalid status')
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        profile = Profile.objects.get(user=request.user)
        validated_data['profile'] = profile

        return super().create(validated_data)

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
    '''
class StatSerializer(serializers.Serializer):
    total_bookings = serializers.IntegerField()
    jobs_completed = serializers.IntegerField()
    ratings = serializers.IntegerField()'''