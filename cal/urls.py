from django.urls import path, re_path
from . import views

app_name = "cal"
urlpatterns = [
    path(r"events/", views.index, name="index"),
    path(r"calendar/", views.CalendarView.as_view(), name="calendar"),
    path(r"event/new/", views.event, name="event_new"),
    re_path(r"event/edit/(?P<event_id>\d+)/", views.event, name="event_edit"),
]
