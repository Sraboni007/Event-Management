from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('', views.home, name='home'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('create-event/', views.create_event, name='create_event'),
    path('update-event/<int:event_id>/', views.update_event, name='update_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('booked-events/', views.booked_events, name='booked_events'),
]
