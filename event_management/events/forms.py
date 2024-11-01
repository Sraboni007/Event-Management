from django import forms
from django.contrib.auth.models import User
from .models import Event
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'location', 'description', 'category', 'booking_limit']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        
        # Check if the date is None
        if date is None:
            raise ValidationError("This field is required.")
        
        # Check if the date is in the past
        if date < timezone.now():
            raise ValidationError("The event date cannot be in the past.")
        
        return date

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
