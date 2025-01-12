import calendar
from datetime import datetime, timedelta, date
import json
import pdb

from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .utils import Calendar
from .forms import EventForm


@csrf_exempt
def index(request):
    if request.content_type == "application/json":
        if request.method == "GET":
            objs = [model_to_dict(e) for e in Event.objects.all()]
            return JsonResponse({"events": objs})
        if request.method == "POST":
            body = request.body.decode("utf-8")
            newest = json.loads(body)
            e = Event(**newest)
            e.start_time = datetime.datetime.fromisoformat(e.start_time)
            e.save()
            return JsonResponse({"newestEvent": model_to_dict(e)}, status=201)

    return HttpResponse("json, please?")


class CalendarView(generic.ListView):
    model = Event
    template_name = "cal/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("cal:calendar"))
    return render(request, "cal/event.html", {"form": form})
