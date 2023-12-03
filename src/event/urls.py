from django.urls import path
from event import views

urlpatterns = [
    path('create-event', views.create_event, name='create_event'),
    path('view-events', views.get_events, name='get_events'),
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('create-weather/<int:coordinate_id>/', views.create_weather, name='create_weather'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
]
