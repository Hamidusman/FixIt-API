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
    reviewer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Rating
        fields = ['id', 'booking', 'rating', 'comment', 'reviewer']
        read_only_fields = ['reviewer']

    def validate_rating(self, value):
        # Ensure the rating is between 1 and 5
        if not (1 <= value <= 5):
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value

    def validate_booking(self, value):
        # Ensure that the booking is completed before allowing a rating
        # Ensure that there’s no existing rating for the booking
        if Rating.objects.filter(booking=value).exists():
            raise serializers.ValidationError("This booking already has a rating.")
        return value