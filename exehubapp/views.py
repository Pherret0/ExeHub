from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from exehubapp.models import *
from django.db import connection


# Create your views here.

def index(request):
    context = {
        "data": ["A man in has fallen into the river in lego city!", "James has used an object!", 1, 2, 3, 4, 5],
    }
    return render(request, 'index.html', context)


def cat(request):
    return render(request, 'cat.html')


@csrf_exempt
def addEvent(request):
    return render(request, 'addevent.html')


@csrf_exempt
def createGroup(request):
    return render(request, 'creategroup.html')


@csrf_exempt
def createEvent(request):
    """
    Currently a test function- final functionality should NOT look like this
    Currently creates a new group if one does not already exist (which is hardcoded), which can be used as the
    group attribute for the event. Takes values from HTML form for creating event and saves to db.
    NOTE: Event group will correspond to the correct group when this is set up.
    NOTE: Owner will correspond to the user logged in, once this is set up.
    """

    try:
        group = ExehubappGroup.objects.get(group_id=1)
    except:
        group_name = 'Test Group'
        group_owner = 'Test'
        group_email = 'Test@hotmail.com'
        group_irc = '696969'
        fee = '6969696'
        group_record = group = ExehubappGroup(group_name=group_name, group_owner=group_owner, group_email=group_email,
                                        group_irc=group_irc, fee=fee)
        group_record.save()

    # Get user input from HTML form
    name = request.POST.get('event_name')
    owner = request.POST.get('owner')
    start = request.POST.get('start')
    end = request.POST.get('end')
    location = request.POST.get('location')
    description = request.POST.get('description')
    min_attendees = request.POST.get('attendees_min')
    max_attendees = request.POST.get('attendees_max')
    record = ExehubappEvent(event_name=name, description=description, event_owner=owner, group=group, start=start,
                            end=end, location=location, attendees_min=min_attendees, attendees_max=max_attendees)
    record.save()
    return HttpResponse("Success!")


def viewAllEvents(request):
    # Select all the events from the events table and save them into a dictionary, pass to the showevents template
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM events")
        data = dictfetchall(cursor)
        context = {
            'data': data
        }
    return render(request, 'showevents.html', context)


def viewEventDetails(request, event_id):
    # Select the event from the events table with corresponding event_id and pass to the event template
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM events WHERE event_id=%s", (event_id,))
        row = cursor.fetchone()
        if not row:
            # If there is no event with the event_id specified, redirect to the home page.
            return render(request, 'index.html')

        context = {
            'data': row
        }
        print(row)
    return render(request, 'event.html', context)


def dictfetchall(cursor):
    # Returns all rows from a cursor as a dictionary
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
