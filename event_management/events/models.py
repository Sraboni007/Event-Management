# events/models.py
from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('conference', 'Conference'),
        ('concert', 'Concert'),
        ('workshop', 'Workshop'),
    ]
    
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_limit = models.PositiveIntegerField(default=100)
    current_bookings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def is_fully_booked(self):
        return self.current_bookings >= self.booking_limit

class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.event.name}"
