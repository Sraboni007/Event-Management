
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Booking
from django.utils import timezone
from .forms import EventForm, UserUpdateForm, UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def home(request):
    events = Event.objects.all()
    booked_events = []
    if request.user.is_authenticated:
        booked_events = Booking.objects.filter(user=request.user).values_list('event_id', flat=True)
    return render(request, 'home.html', {'events': events, 'booked_events': booked_events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_booked = False
    if request.user.is_authenticated:
        is_booked = Booking.objects.filter(event=event, user=request.user).exists()
    return render(request, 'event_detail.html', {'event': event, 'is_booked': is_booked})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form, 'title': 'Create Event'})


@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.created_by != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to edit this event.")
        return redirect('home')
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('home')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form, 'title': 'Update Event'})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.created_by == request.user or request.user.is_staff:
        event.delete()
        messages.success(request, "Event deleted successfully!")
    else:
        messages.error(request, "You do not have permission to delete this event.")
    return redirect('home')


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if Booking.objects.filter(event=event, user=request.user).exists():
        messages.info(request, "You have already booked this event.")
    elif event.is_fully_booked():
        messages.error(request, "Event is fully booked!")
    else:
        Booking.objects.create(event=event, user=request.user)
        event.current_bookings += 1
        event.save()
        messages.success(request, "Successfully booked the event!")
    return redirect('home')

@login_required
def booked_events(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booked_events.html', {'bookings': bookings})
