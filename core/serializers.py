from rest_framework import serializers



class StatSerializer(serializers.Serializers):
    total_bookings = serializers.IntegerField()
    jobs_completed = serializers.IntegerField()
    ratings = serializers.IntegerField()