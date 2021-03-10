from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
import base64
import hashlib
import json
from django.db.models import F
import base64

import random
import string

from django.contrib.auth.decorators import login_required


# Define the web app views
def getProfile(request):
    try:
        pic_id = Users.objects.get(user_id=request.session['user_id']).pic_id
        print(pic_id)
        if not pic_id:

            pic_url = "static/exehubapp/pfp/default.png"
        else:
            pic_url = Pics.objects.get(pic_id=pic_id).pic

        return pic_url

    except:
        return " "


def index(request):
    """
    View to display the index.html template.
    Passes the the context dictionary with data to be displayed.
    """

    try:
        id = request.session['user_id']
    except:
        return render(request, 'login.html')

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM posts")  # getting posts
        data = dictfetchall(cursor)  # putting it int a dict

        for row in data:
            post_owner = row['post_owner']
            user_id = row['user_id']

            if not user_id:

                with connection.cursor() as cursor:
                    cursor.execute("UPDATE posts set user_id=1 where post_id IS NULL")  # getting posts
                pic_url = "static/exehubapp/pfp/default.png"

            else:
                pic_id = Users.objects.get(user_id=user_id).pic_id
                if not pic_id:
                    pic_url = "static/exehubapp/pfp/default.png"
                else:
                    pic_url = Pics.objects.get(pic_id=pic_id).pic


            row['poster_pfp'] = pic_url


        try:
            # pic_id = Users.objects.get(user_id=request.session['user_id']).pic_id
            # pic_url = Pics.objects.get(pic_id=pic_id).pic

            pic_url = getProfile(request)

            if pic_url == " ":
                context = {
                    'data': data,
                }
            else:
                user_id = request.session['user_id']
                context = {
                    'data': data,
                    'user_id': user_id,
                    'pfp': pic_url,
                }

        except:
            context = {
                'data': data,
            }
    return render(request, 'index.html', context)


@csrf_exempt
def profile(request):
    """
    View to display the profile.html template.
    """

    try:
        id = request.session['user_id']
    except:
        return render(request, 'login.html')

    if request.POST.get("logout"):
        del request.session['user_id']
        return render(request, 'login.html')
    elif request.POST.get("uploadProfilePic"):
        image = request.FILES["image"]
        form = ProfilePicForm(request.POST, request.FILES)
        record = Pics(pic=image)
        record.save()
        pic_id = record.pic_id
        user = Users.objects.get(user_id=request.session['user_id'])
        user.pic_id = pic_id
        user.save()
    else:
        form = ProfilePicForm()

    user = Users.objects.get(user_id=request.session['user_id'])
    members = Members.objects.filter(user=user).values_list('group')

    group_list = []
    for i in members:
        group_list.append(i[0])

    groups = UniGroups.objects.filter(group_id__in=group_list).values_list('group_name', 'fee', 'group_email')

    pic_url = getProfile(request)

    if pic_url == " ":
        context = {'user': user, 'groups': groups, 'form': form}
    else:

        user_id = request.session['user_id']
        context = {'user': user, 'groups': groups, 'form': form,
                   'user_id': user_id,
                   'pfp': pic_url, }

    return render(request, 'profile.html', context)


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

    try:
        id = request.session['user_id']
    except:
        return render(request, 'login.html')

    user_id = request.session['user_id']
    user = Users.objects.get(user_id=user_id)
    post_owner = user.name

    if request.method == 'POST':
        try:
            image = request.FILES['image']
        except:
            image = ""

        post_name = request.POST['post_name']
        start = request.POST['start']
        end = request.POST['end']
        description = request.POST['description']
        attendees_min = request.POST['attendees_min']
        attendees_max = request.POST['attendees_max']
        location = request.POST['location']
        type = request.POST['type']

        postAch(request)
        form = DocumentForm(request.POST, request.FILES, user_id=user_id)
        record = Posts(post_name=post_name, start=start, post_owner=post_owner, end=end,
                       description=description, attendees_min=attendees_min,
                       attendees_max=attendees_max, location=location, type=type,
                       group=UniGroups.objects.get(group_id=1), image=image)


        postAch(request)
        record.save()

        post_id = record.post_id
        with connection.cursor() as cursor:
            print("Updating user id")
            print(user_id)
            print(post_id)
            cursor.execute("UPDATE posts SET user_id=%s WHERE post_id=%s", (user_id, post_id,))

        id = record.post_id

        try:
            user = Users.objects.get(user=user)
        except:
            user = ""

        if type == "event" and user != "":
            event = Posts.objects.get(post_id=id)
            attendee_record = Attendees(user=user, event=event)
            attendee_record.save()

    else:
        form = DocumentForm(user_id=user_id)

    # Get all of users groups
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM uni_groups")
        data = dictfetchall(cursor)

        pic_url = getProfile(request)

        if pic_url == " ":

            context = {
                'data': data, 'form': form
            }
        else:

            user_id = request.session['user_id']
            context = {'data': data, 'form': form,
                       'user_id': user_id,
                       'pfp': pic_url}

        return render(request, 'addevent.html', context)


@csrf_exempt
def createGroup(request):
    """
    View to display the creategroup.html template.
    """

    try:
        id = request.session['user_id']
    except:
        return render(request, 'login.html')

    return render(request, 'creategroup.html')


def viewAllEvents(request):
    """
    View to display the showevents.html template.
    Passes the the context dictionary with data with events
    data to the template to be displayed
    """

    try:
        id = request.session['user_id']
    except:
        return render(request, 'login.html')

    # Select all the events from the events table
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM posts")
        data = dictfetchall(cursor)

        pic_url = getProfile(request)

        if pic_url == " ":
            context = {'data': data}
        else:

            user_id = request.session['user_id']
            context = {'data': data, 'user_id': user_id,
                       'pfp': pic_url}

    return render(request, 'showevents.html', context)


def viewEventDetails(request, post_id):
    """
    View to display the event.html template.
    Passes the the context dictionary with data about the individual
    event to be displayed in the template.
    """

    try:
        id = request.session['user_id']
    except:
        return render(request, 'login.html')

    # Select the event from the events table with corresponding event_id
    # and pass to the event template
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM posts WHERE post_id=%s", (post_id,))
        row = cursor.fetchone()
        if not row:
            # If there is no event with the event_id specified, redirect to the home page.
            return render(request, 'index.html')

        context = {
            'data': row
        }

    return render(request, 'event.html', context)


def getViewGroupsData(request):
    user = Users.objects.get(user_id=request.session['user_id'])

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM members WHERE user_id=%s", (str(user.user_id)), )
        data = cursor.fetchall()

    group_list = []
    for i in data:
        group_list.append(i[2])

    print(group_list)

    groups = UniGroups.objects.all().exclude(group_id__in=group_list).values_list('group_id', 'group_name', 'fee',
                                                                                  'group_email')

    in_groups = UniGroups.objects.filter(group_id__in=group_list).values_list('group_id', 'group_name', 'fee',
                                                                              'group_email')

    print(in_groups)
    print(groups)

    pic_url = getProfile(request)

    if pic_url == " ":
        return {'outgroups': groups, 'ingroups': in_groups}
    else:

        user_id = request.session['user_id']
        return {'outgroups': groups, 'ingroups': in_groups, 'user_id': user_id,
                'pfp': pic_url}


def viewGroups(request):
    """
    View to display the showgroups.html template.
    Passes the the context dictionary with data to be displayed.
    """

    try:
        id = request.session['user_id']
    except:
        return render(request, 'login.html')

    # Select all the events from the events table and save them into a dictionary,
    # pass to the showevents template

    context = getViewGroupsData(request)
    return render(request, 'showgroups.html', context)


def joinGroup(request, group_id):
    group = UniGroups.objects.get(group_id=group_id)
    user = Users.objects.get(user_id=request.session['user_id'])
    member_record = Members(user=user, group=group, is_group_admin=0)
    member_record.save()

    context = getViewGroupsData(request)
    return render(request, 'showgroups.html', context)


def leaveGroup(request, group_id):
    group = UniGroups.objects.get(group_id=group_id)
    user = Users.objects.get(user_id=request.session['user_id'])

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM members WHERE user_id=%s and group_id=%s",
                       (str(user.user_id), str(group.group_id),))

    context = getViewGroupsData(request)
    return render(request, 'showgroups.html', context)


def viewAchs(request):
    """
    View to display the showgroups.html template.
    Passes the the context dictionary with data to be displayed.
    """
    # Select all the events from the events table and save them into a
    # dictionary, pass to the showevents template
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM achievements")
        data = dictfetchall(cursor)

        pic_url = getProfile(request)

        if pic_url == " ":
            context = {'data': data}
        else:

            user_id = request.session['user_id']
            context = {'data': data, 'user_id': user_id,
                       'pfp': pic_url}

    return render(request, 'showachs.html', context)


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

    # Select all the events from the events table and save them into a dictionary,
    # pass to the showevents template
    with connection.cursor() as cursor:
        cursor.execute("SELECT email,password_hash FROM users "
                       "WHERE email=%s AND password_hash=%s",
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

    # Get data from form
    fname = request.POST.get('fname')
    name = request.POST.get('name')
    email = request.POST.get('email')
    dob = request.POST.get('dob')

    password = request.POST.get('password')

    # Generate salt
    salt = ''.join([random.choice(string.ascii_letters) for i in range(16)])
    salted_password = salt + password

    # Hash the password
    hash_sha3_512 = hashlib.new("sha3_512", salted_password.encode())
    pswd = hash_sha3_512.digest()

    # Concatenate first and last name
    fullName = fname + " " + name

    # Save new user to the Model.
    record = Users(is_server_admin=False, date_of_birth=dob, email=email,
                   name=fullName, password_hash=pswd, salt=salt)

    record.save()

    return HttpResponse("Success!")


@csrf_exempt
def validateLogin(request):
    """
    Function to check the user's login data compared to the database
    """

    email = request.POST.get('email')

    # Check email is in database
    if Users.objects.filter(email=email).count() != 0:
        user = Users.objects.get(email=email)

        # Get the hashed password and salt
        user_password = user.password_hash
        user_salt = user.salt

        # Hash user input
        password = request.POST.get('password')
        salted_password = user_salt + password
        hash_sha3_512 = hashlib.new("sha3_512", salted_password.encode())
        pswd = hash_sha3_512.digest()
        pswd = bytearray(pswd)

        # Compare user input to password
        if user_password == pswd:
            request.session['user_id'] = user.user_id
            print(request.session['user_id'])
            return HttpResponse(0)
        else:
            return HttpResponse(1)
    else:
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

    # Get the owner of the group using the session variable
    try:
        group_owner = Users.objects.get(user_id=request.session['user_id'])
        group_owner_name = group_owner.name
    except:
        # If not logged in set owner name to empty string
        group_owner = ""
        group_owner_name = ""

    # If no fee is entered, set fee to 0
    if fee == "":
        fee = 0

    record = UniGroups(group_name=group_name, group_owner=group_owner_name,
                       group_email=group_email, fee=fee)

    # Save the group to the Model
    groupAch(request)
    record.save()

    group = UniGroups.objects.get(group_name=group_name)
    member_record = Members(user=group_owner, group=group, is_group_admin=1)
    member_record.save()

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


def test(request):
    """
    View to display the test.html template.
    """
    return render(request, 'test.html')


def leaderboard(request):
    """
    View to show the leaderboard
    """
    try:
        id = request.session['user_id']
    except:
        return render(request, 'login.html')

    # with connection.cursor() as cursor:
    #    cursor.execute("SELECT * FROM events")
    #    data = dictfetchall(cursor)
    #    context = {
    #        'data': data
    #    }
    # return render(request, 'showevents.html', context)

    data = [{"Name": "James", "Points": 50}, {"Name": "Travis", "Points": 40}, {"Name": "Kai", "Points": 35},
            {"Name": "Jack", "Points": 30}, {"Name": "Ellie", "Points": 25}, {"Name": "Georgia", "Points": 5}]

    pic_url = getProfile(request)

    if pic_url == " ":
        context = {'data': data}
    else:

        user_id = request.session['user_id']
        context = {'data': data, 'user_id': user_id,
                   'pfp': pic_url}

    return render(request, 'leaderboard.html', context)


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
        # Return 0 if group name free to use
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

    # Get password stored in db
    user = Users.objects.get(user_id=request.session['user_id'])
    salt = user.salt
    correct_password = user.password_hash

    # Get form data submitted
    email = request.POST.get('email')
    password = request.POST.get('password')
    password = salt + password

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
        Users.objects.filter(user_id=request.session['user_id']).update(email=email)

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

    # Get password stored in db
    user = Users.objects.get(user_id=request.session['user_id'])
    salt = user.salt
    stored_password = user.password_hash

    # Get entered data from form
    current_password = request.POST.get('current_password')
    current_password = salt + current_password
    new_password = request.POST.get('new_password')
    new_password = salt + new_password

    # Get the hash of the entered current password
    hashed_current_password = hashlib.new("sha3_512", current_password.encode())
    hashed_current_password = hashed_current_password.digest()
    hashed_current_password = bytearray(hashed_current_password)

    # Check entered password is correct
    if hashed_current_password != stored_password:
        # If password incorrect, return 2
        return HttpResponse(2)

    # Get the hashed new password
    new_password_hashed = hashlib.new("sha3_512", new_password.encode())
    new_password_hashed = new_password_hashed.digest()

    # Update the users password
    try:
        Users.objects.filter(user_id=request.session['user_id']).update(password_hash=new_password_hashed)
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

    # Get password stored in db
    user = Users.objects.get(user_id=request.session['user_id'])
    salt = user.salt
    stored_password = user.password_hash

    # Hash entered password
    password = request.POST.get('password')
    password = salt + password
    hashed_password = hashlib.new("sha3_512", password.encode())
    hashed_password = hashed_password.digest()
    hashed_password = bytearray(hashed_password)

    # Check entered password is correct
    if hashed_password != stored_password:
        # If password incorrect, return 2
        return HttpResponse(2)

    try:
        # If user deleted successfully, return 0
        user.delete()
        del request.session['user_id']
        return HttpResponse(0)
    except:
        # If error in deleting user, return 1
        return HttpResponse(1)


@csrf_exempt
def post(request, post_id):
    """
    Displays an individual post and comments
    """
    """
    print(post_id)
    post = Posts.objects.get(post_id=post_id)  # check for injections here
    print(post)
    if not post:
        # If there is no postt with the post_id specified, redirect to the home page.
        return render(request, 'index.html')
    print(post.post_name)
    # if post.image:
    #    with open(post.image, "rb") as image_file:
    #        image_decoded = base64.b64encode(image_file.read()).decode('utf-8')
    #    post.image = image_decoded
    context = {
        'post': post
    }
    """

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM posts WHERE post_id=%s", (post_id,))
        data = dictfetchall(cursor)
        print(data)
        context = {
            'data': data
        }
    return render(request, 'post.html', context)


@csrf_exempt
def upvote(request):
    """
    Increments an upvote if user hasn't clicked before, else it decrements it
    """
    post_id = request.POST.get('post_id')
    user_id = request.session['user_id']
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM upvotes WHERE user_id = %s AND post_id = %s", (user_id, post_id))
            data = dictfetchall(cursor)
            print(data)
        # Posts.objects.filter(post_id=id).update(upvote=F('upvote') + 1)
        if data:
            # user has already upvoted
            print("User has upvoted")
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(user_id) FROM upvotes WHERE post_id = %s", (post_id,))
                data = cursor.fetchall()
                upvote_num = data[0][0]
                cursor.execute("DELETE FROM upvotes WHERE user_id = %s AND post_id = %s ", (user_id, post_id,))
            upvote_num -= 1
            print("Changing upvote by -1")
            return HttpResponse(upvote_num)

        else:
            # user has not upvoted
            print("User has not upvoted yet")
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(user_id) FROM upvotes WHERE post_id = %s", (post_id,))
                data = cursor.fetchall()
                print(data)
                upvote_num = data[0][0]
                cursor.execute("INSERT INTO upvotes VALUES (%s, %s)", (user_id, post_id))
            upvote_num += 1
            print(upvote_num)
            print("Changing upvote by + 1")
            return HttpResponse(upvote_num)

    # If update successful, return 0
    # If update unsuccessful, return 1
    except Exception:
        print("Fail")
        return HttpResponse(-1)


@csrf_exempt
def postAch(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM achievements where ach_name = \"Something to Share\"")
        data = dictfetchall(cursor)
        context = {
            'data': data
        }

        if data:
            postAch10(request)
        else:
            cursor.execute(
                "INSERT INTO achievements(ach_name, requirement, value) VALUES (\"Something to Share\", \"Make 1 post\", 10)")
    return render(request, 'showgroups.html', context)


@csrf_exempt
def postAch10(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM achievements where ach_name = \"Postal worker\"")
        data = dictfetchall(cursor)
        context = {
            'data': data
        }

        if data:
            postAch50(request)
        else:
            user_id = request.session["user_id"]
            user = Users.objects.get(user_id=user_id)
            post_num = Posts.objects.filter(post_owner=user.name).count()
            if post_num >= 10:
                cursor.execute(
                    "INSERT INTO achievements(ach_name, requirement, value) VALUES (\"Postal worker\", \"Make 10 posts\", 10)")
    return render(request, 'showgroups.html', context)


@csrf_exempt
def postAch50(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM achievements where ach_name = \"Post office manager\"")
        data = dictfetchall(cursor)
        context = {
            'data': data
        }

        if data:
            postAch100(request)
        else:
            user_id = request.session["user_id"]
            user = Users.objects.get(user_id=user_id)
            post_num = Posts.objects.filter(post_owner=user.name).count()
            if post_num >= 50:
                cursor.execute(
                    "INSERT INTO achievements(ach_name, requirement, value) VALUES (\"Post office manager\", \"Make 50 posts\", 50)")
    return render(request, 'showgroups.html', context)


@csrf_exempt
def postAch100(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM achievements where ach_name = \"Lord of posts\"")
        data = dictfetchall(cursor)
        context = {
            'data': data
        }
        print(data)
        if not data:
            user_id = request.session["user_id"]
            user = Users.objects.get(user_id=user_id)
            post_num = Posts.objects.filter(post_owner=user.name).count()
            if post_num >= 100:
                cursor.execute(
                    "INSERT INTO achievements(ach_name, requirement, value) VALUES (\"Lord of posts\", \"Make 100 posts\", 50)")
    return render(request, 'showgroups.html', context)


def groupAch(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM achievements where ach_name = \"United we stand\"")
        data = dictfetchall(cursor)
        context = {
            'data': data
        }

        if not data:
            cursor.execute(
                "INSERT INTO achievements(ach_name, requirement, value) VALUES (\"United we stand\", \"Make 1 group\", 10)")
    return render(request, 'showgroups.html', context)
