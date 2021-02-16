from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from exehubapp.models import *


# Create your views here.

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def addEvent(request):
    return render(request, 'addevent.html')

@csrf_exempt
def createEvent (request):
    """
    Currently a test function- final functionality should NOT look like this
    Currently creates a brand new group (which is hardcoded) so that the group can be passed to the event
    Event attributes are also hardcoded and must be taken from the POST request after the addevent page is created
        properly to reflect the database.

    """
    group_name = 'Big Trucks big bucks'
    group_owner = 'Dave'
    group_email = 'Dave@hotmail.com'
    group_irc = '696969'
    fee = '6969696'
    record = group = Group(group_name=group_name, group_owner=group_owner, group_email=group_email, group_irc=group_irc,
                  fee=fee)
    record.save()

    print("Hello")
    name = request.POST.get('eventname')
    owner = 'me'
    group = group
    start_date_time = '2020-12-05 12:12:12'
    end_date_time = '2021-12-12 12:12:12'
    location = 'london'
    description = request.POST.get('desc')
    min_attendees = 0
    max_attendees = 1
    record = Event(name=name, description=description, owner=owner, group=group, start_date_time=start_date_time,
                   end_date_time=end_date_time, location=location, min_attendees=min_attendees,
                   max_attendees=max_attendees)
    record.save()
    return HttpResponse("success!")

def viewEvents(request):
    return render(request, 'events.html')

