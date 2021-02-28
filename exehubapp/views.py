from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from exehubapp.models import *
from django.db import connection
import hashlib


# Create your views here.

def index(request):
    context = {
        "data": ["A man in has fallen into the river in lego city!", "James has used an object!", 1, 2, 3, 4, 5],
    }
    return render(request, 'index.html', context)


def cat(request):
    return render(request, 'cat.html')


@csrf_exempt
def register(request):
    return render(request, 'register.html')


@csrf_exempt
def addUser(request):
    fname = request.POST.get('fname')
    name = request.POST.get('name')
    email = request.POST.get('email')
    dob = request.POST.get('dob')
    password = request.POST.get('password')
    hash_sha3_512 = hashlib.new("sha3_512", password.encode())
    pswd = hash_sha3_512.digest()
    fullName = fname + " " + name
    record = Users (is_server_admin=False, date_of_birth=dob, email=email, name=fullName, password_hash=pswd)
    record.save()
    return HttpResponse("Success!")

@csrf_exempt
def addEvent(request):
    return render(request, 'addevent.html')


@csrf_exempt
def createGroup(request):
    return render(request, 'creategroup.html')

@csrf_exempt
def createGroupForm(request):
    """
    Currently a test function- final functionality should NOT look like this
    Currently creates a new group if one does not already exist (which is hardcoded), which can be used as the
    group attribute for the event. Takes values from HTML form for creating event and saves to db.
    NOTE: Event group will correspond to the correct group when this is set up.
    NOTE: Owner will correspond to the user logged in, once this is set up.
    """

    # Get user input from HTML form
    group_name = request.POST.get('group_name')
    group_owner = request.POST.get('group_owner')
    group_email = request.POST.get('group_email')
    fee = request.POST.get('fee')
    record = UniGroups(group_name=group_name, group_owner=group_owner, group_email=group_email, fee=fee)
    record.save()
    return HttpResponse("Success!")


@csrf_exempt
def createEvent(request):
    """
    Currently a test function- final functionality should NOT look like this
    Currently creates a new group if one does not already exist (which is hardcoded), which can be used as the
    group attribute for the event. Takes values from HTML form for creating event and saves to db.
    NOTE: Event group will correspond to the correct group when this is set up.
    NOTE: Owner will correspond to the user logged in, once this is set up.
    """

    # Get user input from HTML form
    name = request.POST.get('event_name')
    owner = request.POST.get('owner')
    group = UniGroups.objects.get(group_id=1)
    start = request.POST.get('start')
    end = request.POST.get('end')
    location = request.POST.get('location')
    description = request.POST.get('description')
    min_attendees = request.POST.get('attendees_min')
    max_attendees = request.POST.get('attendees_max')
    record = Events(event_name=name, description=description, event_owner=owner, group=group, start=start,
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

def viewGroups(request):
    # Select all the events from the events table and save them into a dictionary, pass to the showevents template
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM uni_groups")
        data = dictfetchall(cursor)
        context = {
            'data': data
        }
    return render(request, 'showgroups.html', context)


def dictfetchall(cursor):
    # Returns all rows from a cursor as a dictionary
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
