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
        fields = ['id', 'profile', 'service', 'phone_number', 'price', 'description',
            'region', 'address', 'state',
            'date', 'time', 'duration',
            'created_at', 'status'
            ]
        read_only_fields = ['profile', 'created_at']

    def validate_status(self, value):
        if value not in dict(Booking.STATUS_CHOICES):
            return serializers.ValidationError('Invalid status')
        return value
    
    
    def calculate_price(self, duration):
        # Pricing rules for different intervals
        rates = {
            15: 10,   # $10 for 15 minutes
            30: 18,   # $18 for 30 minutes
            45: 25,   # $25 for 45 minutes
            60: 30    # $30 for 60 minutes
        }
        base_rate = 5  # Additional charge for durations exceeding 60 minutes

        if duration in rates:
            return rates[duration]
        elif duration > 60:
            # Charge based on the nearest interval + base_rate
            extra_minutes = duration - 60
            extra_charges = (extra_minutes // 15) * base_rate
            return rates[60] + extra_charges
        else:
            raise serializers.ValidationError("Invalid duration. Must be 15, 30, 45, or 60 minutes.")


    def create(self, validated_data):
        duration = validated_data.get('duration')
        validated_data['price'] = self.calculate_price(duration)
        
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