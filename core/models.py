from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User

from users.models import Profile
# Create your models here.

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=True)
    phone_number = models.CharField(max_length=15, verbose_name=_('phone number'))
    description = models.TextField()
    address = models.CharField(max_length=100)
    region = models.CharField(max_length=20, default='abuja')
    state = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    duration = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=25)
    
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),  # Queries by user
            models.Index(fields=['status']),  # Queries by status
            models.Index(fields=['user', 'status']),  # Combined filters
        ]
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')

    def __str__(self):
        return f'Booking for {self.service}'

class Rating(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rating by {self.reviewer} for booking {self.booking.id}'