from rest_framework import serializers
from .models import Booking, Rating

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'service', 'phone_number', 'price', 'description',
            'region', 'address', 'state',
            'date', 'time', 'duration',
            'created_at', 'status'
            ]
        read_only_fields = ['user', 'created_at']

    def validate_status(self, value):
        if value not in dict(Booking.STATUS_CHOICES):
            return serializers.ValidationError('Invalid status')
        return value
    
    
    def calculate_price(self, duration):
        base_rate = 10
        if duration is None or duration < 15:
            raise ValueError("Duration must be at least 15 minutes.")
        return base_rate + ((duration - 15) // 15) * 2

    def create(self, validated_data):
        duration = validated_data.get('duration')
        validated_data['price'] = self.calculate_price(duration)
        
        request = self.context.get('request')
        user=request.user
        validated_data['user'] = user
        return super().create(validated_data)

class RatingSerializer(serializers.ModelSerializer):
    reviewer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Rating
        fields = ['booking', 'rating', 'comment', 'reviewer']
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