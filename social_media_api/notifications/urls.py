from django.urls import path
from .views import get_notifications

urlpatterns = [
    path('notifications/', get_notifications, name='get_notifications'),
]
