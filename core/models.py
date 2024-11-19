from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

from users.models import Profile
# Create your models here.

class Service(models.Model):
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    base_rate = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('base rate'))

    def __str__(self):
        return self.category

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    service = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=True)
    phone_number = models.IntegerField(verbose_name=_('phone number'))
    description = models.TextField()
    address = models.CharField(max_length=100)
    region = models.CharField(max_length=20, default='abuja')
    state = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=25)

    def __str__(self):
        return {f'Booking for {self.service} by {self.firstname}+{self.lastname}'}

class Rating(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rating by {self.reviewer} for booking {self.booking.id}'