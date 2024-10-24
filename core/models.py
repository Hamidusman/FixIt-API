from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Profile
# Create your models here.

class Service(models.Model):
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    base_rate = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('base rate'))

    def __str__(self):
        return self.category

class Booking(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    phone_number = models.IntegerField(verbose_name=_('phone number'))
    description = models.TextField()
    address = models.CharField(max_length=100)
    region = models.CharField(max_length=20, default='abuja')
    state = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    #status = models.CharField(choices=)

    def __str__(self):
        return {f'Booking for {self.service.category} by {self.firstname}+{self.lastname}'}

class Rating(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField

    def __str__(self):
        return self.comment