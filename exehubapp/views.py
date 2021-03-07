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


def profile(request):
    """
    View to display the profile.html template.
    """
    return render(request, 'profile.html')


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

    # Get all of users groups
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM uni_groups")
        data = dictfetchall(cursor)
        context = {
            'data': data
        }

    return render(request, 'addevent.html', context)


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

    #Get data from form
    fname = request.POST.get('fname')
    name = request.POST.get('name')
    email = request.POST.get('email')
    dob = request.POST.get('dob')

    # Hash the password
    password = request.POST.get('password')
    hash_sha3_512 = hashlib.new("sha3_512", password.encode())
    pswd = hash_sha3_512.digest()

    # Concatenate first and last name
    fullName = fname + " " + name

    # Save new user to the Model.
    record = Users(is_server_admin=False, date_of_birth=dob, email=email, name=fullName, password_hash=pswd)
    record.save()

    return HttpResponse("Success!")


@csrf_exempt
def createEvent(request):
    """
    Function to request the data from the create
    event form and save to the database.
    """

    # Get entered data from form
    type = request.POST.get('type')
    name = request.POST.get('event_name')
    description = request.POST.get('description')
    owner = request.POST.get('owner')

    # Get the group object from the Model using the
    # group selected in the form
    group_input = request.POST.get('group')
    group = UniGroups.objects.get(group_name=group_input)

    if type == "event":
        start = request.POST.get('start')
        end = request.POST.get('end')
        location = request.POST.get('location')
        min_attendees = request.POST.get('attendees_min')
        max_attendees = request.POST.get('attendees_max')
        record = Events(event_name=name, description=description, event_owner=owner, group=group, start=start,
                        end=end, location=location, attendees_min=min_attendees, attendees_max=max_attendees)

    elif type == "text":
        record = Events(event_name=name, description=description, event_owner=owner, group=group)

    elif type =="image":
        image = request.POST.get('image')
        record = Events(event_name=name, description=description, event_owner=owner, group=group, image=image)

    else:
        return HttpResponse(1)

    try:
        record.save()
        return HttpResponse(0)
    except:
        return HttpResponse(1)


@csrf_exempt
def createGroupForm(request):
    """
    Function to request the data from the create
    group form and save to the database.
    """

    # Get user input from HTML form
    group_name = request.POST.get('group_name')
    group_email = request.POST.get('group_email')
    fee = request.POST.get('fee')

    # Get the user id from the hidden input field
    group_owner_id = request.POST.get('group_owner')

    # Get the user object
    owner = Users.objects.get(user_id=group_owner_id)

    # Get the user name and use for group owner
    group_owner_name = owner.name

    # If no fee is entered, set fee to 0
    if fee == "":
        fee = 0

    record = UniGroups(group_name=group_name, group_owner=group_owner_name, group_email=group_email, fee=fee)

    # Save the group to the Model

    record.save()

    # Return 0 if successful
    return HttpResponse(0)



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


@csrf_exempt
def verifyUniqueGroup(request):
    """
    Function to asynchronously check whether the new
    group name is unique using an AJAX call.
    """

    # Get the group name from the form
    groupName = request.POST.get('groupName')

    # Check whether the group name is already in the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM uni_groups WHERE group_name=%s", (groupName,))
        row = cursor.fetchone()

    if row:
        # Return 1 if group name already used
        return HttpResponse(1)
    else:
        #Return 0 if group name free to use
        return HttpResponse(0)
    

@csrf_exempt
def verifyUniqueEmail(request):
    """
    Function to asynchronously check whether the email address
    is unique and not registered already using an AJAX call.
    """

    # Get the email from the form
    email = request.POST.get('email')

    # Check whether the email is unique and not registered already
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        row = cursor.fetchone()

    if row:
        # If email already registered, return 1
        return HttpResponse(1)
    else:
        # If email not registered, return 0.
        return HttpResponse(0)


@csrf_exempt
def updateEmail(request):
    """
    Function to check user entered correct password,
    before updating their email address in the Model.
    """

    # Get form data submitted
    email = request.POST.get('email')
    password = request.POST.get('password')

    # Get the password of the user stored in the db.
    user_id = request.POST.get('user_id')
    user = Users.objects.get(user_id=user_id)
    correct_password = user.password_hash

    # Hash the password the user entered in the form.
    hashed_entered_password = hashlib.new("sha3_512", password.encode())
    hashed_entered_password = hashed_entered_password.digest()
    hashed_entered_password = bytearray(hashed_entered_password)

    # Check user entered correct password
    if hashed_entered_password != correct_password:
        # Return 2 if password incorrect
        return HttpResponse(2)

    # Update users email in the Model.
    try:
        Users.objects.filter(user_id=user_id).update(email=email)

        # Return 0 if update successful
        return HttpResponse(0)
    except:
        # Return 1 if update unsuccessful
        return HttpResponse(1)


@csrf_exempt
def updatePassword(request):
    """
    Function to check user entered their correct old password,
    before updating their password in the Model.
    """

    # Get entered data from form
    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')

    # Get the current user object from the Model
    user_id = request.POST.get('user_id')
    user = Users.objects.get(user_id=user_id)
    stored_password = user.password_hash

    # Get the hash of the entered current password
    hashed_current_password = hashlib.new("sha3_512", current_password.encode())
    hashed_current_password = hashed_current_password.digest()
    hashed_current_password = bytearray(hashed_current_password)

    # Check entered password is correct
    if hashed_current_password!=stored_password:
        # If password incorrect, return 2
        return HttpResponse(2)

    # Get the hashed new password
    new_password_hashed = hashlib.new("sha3_512", new_password.encode())
    new_password_hashed = new_password_hashed.digest()

    # Update the users password
    try:
        Users.objects.filter(user_id=user_id).update(password_hash=new_password_hashed)
        # If update successful, return 0
        return HttpResponse(0)
    except:
        # If update unsuccessful, return 1
        return HttpResponse(1)

@csrf_exempt
def deleteAccount(request):
    """
    Function to delete a user account
    """
    # Hash entered password
    password = request.POST.get('password')
    hashed_password = hashlib.new("sha3_512", password.encode())
    hashed_password = hashed_password.digest()
    hashed_password = bytearray(hashed_password)

    # Get password stored in db
    user_id = request.POST.get('user_id')
    user = Users.objects.get(user_id=user_id)
    stored_password = user.password_hash

    # Check entered password is correct
    if hashed_password != stored_password:
        # If password incorrect, return 2
        return HttpResponse(2)

    try:
        # If user deleted successfully, return 0
        user.delete()
        return HttpResponse(0)
    except:
        #If error in deleting user, return 1
        return HttpResponse(1)


