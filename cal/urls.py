from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    path(r'index/', views.index, name='index'),
    path(r'calendar/', views.CalendarView.as_view(), name='calendar'),
    path(r'event/new/', views.event, name='event_new'),
	path(r'event/edit/(?P<event_id>\d+)/', views.event, name='event_edit'),
]
