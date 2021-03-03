from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db import connection
import hashlib

# Define the web app views


def index(request):
    """
    View to display the index.html template.
    Passes the the context dictionary with data to be displayed.
    """

    context = {
        "data": ["A man in has fallen into the river in lego city!",
                 "James has used an object!", 1, 2, 3, 4, 5],
    }
    return render(request, 'index.html', context)


def cat(request):
    """
    View to display the cat.html template.
    """
    return render(request, 'cat.html')


@csrf_exempt
def register(request):
    """
    View to display the index.html template.
    Passes the the context dictionary with data to be displayed.
    """
    return render(request, 'register.html')


@csrf_exempt
def login(request):
    """
    View to display the login.html template.
    """
    return render(request, 'login.html')


@csrf_exempt
def addEvent(request):
    """
    View to display the addevent.html template.
    """
    return render(request, 'addevent.html')


@csrf_exempt
def createGroup(request):
    """
    View to display the creategroup.html template.
    """

    # Get user input from HTML form
    return render(request, 'creategroup.html')


def viewAllEvents(request):
    """
    View to display the showevents.html template.
    Passes the the context dictionary with data with events
    data to the template to be displayed
    """

    # Select all the events from the events table
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM events")
        data = dictfetchall(cursor)
        context = {
            'data': data
        }
    return render(request, 'showevents.html', context)


def viewEventDetails(request, event_id):
    """
    View to display the event.html template.
    Passes the the context dictionary with data about the individual
    event to be displayed in the template.
    """

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

    return render(request, 'event.html', context)


def viewGroups(request):
    """
    View to display the showgroups.html template.
    Passes the the context dictionary with data to be displayed.
    """
    # Select all the events from the events table and save them into a dictionary, pass to the showevents template
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM uni_groups")
        data = dictfetchall(cursor)
        context = {
            'data': data
        }
    return render(request, 'showgroups.html', context)


def termsConditions(request):
    """
    View to display the termsconditions.html template.
    """
    return render(request, 'termsconditions.html')


# Define functions

@csrf_exempt
def verifyUser(request, email, password_hash):
    """
    Function to check whether the users login
    details are valid.
    """

    # Select all the events from the events table and save them into a dictionary, pass to the showevents template
    with connection.cursor() as cursor:
        cursor.execute("SELECT email,password_hash FROM users WHERE email=%s AND password_hash=%s",
                       (email, password_hash,))
        data = dictfetchall(cursor)
        if data:
            return HttpResponse("Success!")
        else:
            print("Didn't work")


@csrf_exempt
def addUser(request):
    """
    Function to process the submission of the register form.
    Requests data from the register form and saves to the database.
    """
    fname = request.POST.get('fname')
    name = request.POST.get('name')
    email = request.POST.get('email')
    dob = request.POST.get('dob')
    password = request.POST.get('password')
    hash_sha3_512 = hashlib.new("sha3_512", password.encode())
    pswd = hash_sha3_512.digest()
    fullName = fname + " " + name
    record = Users(is_server_admin=False, date_of_birth=dob, email=email, name=fullName, password_hash=pswd)
    record.save()
    return HttpResponse("Success!")


@csrf_exempt
def createEvent(request):
    """
    Function to request the data from the create
    event form and save to the database.
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
    try:
        record.save()
        return HttpResponse("0")
    except:
        return HttpResponse("1")


@csrf_exempt
def createGroupForm(request):
    """
    Function to request the data from the create
    group form and save to the database.
    """

    # Get user input from HTML form
    group_name = request.POST.get('group_name')
    group_owner = request.POST.get('group_owner')
    group_email = request.POST.get('group_email')
    fee = request.POST.get('fee')
    record = UniGroups(group_name=group_name, group_owner=group_owner, group_email=group_email, fee=fee)
    try:
        record.save()
        return HttpResponse("0")
    except:
        return HttpResponse("1")


def dictfetchall(cursor):
    """
    Function to return query from the database in a
    dictionary data structure.
    """
    # Returns all rows from a cursor as a dictionary
    desc = cursor.description

    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
