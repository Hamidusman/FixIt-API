from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Service(models.Model):
    specialty = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to=('images'))
    rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.specialty

class Booking(models.Model):
    firstname = models.CharField(max_length=20, verbose_name=_('first name'))
    lastname = models.CharField(max_length=20, verbose_name=_('last name'))
    phone_number = models.IntegerField(verbose_name=_('phone number'))
    email = models.EmailField()
    address = models.CharField(max_length=100)
    region = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    #status = models.CharField(choices=)

    def __str__(self):
        return {f'Booking for {self.service.specialty} by {self.firstname}+{self.lastname}'}

class Rating(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField

    def __str__(self):
        return self.comment