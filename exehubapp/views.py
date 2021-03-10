from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forms import *
import hashlib
import json
import random
import string

# Define the web app views

@csrf_exempt
def index(request):
    """
    View to display the index.html template.
    Passes the the context dictionary with data to be displayed.
    """

    try:
        # Gets the user ID if they are logged in
        user_id = request.session['user_id']
    except:
        # If the user is not logged in, get posts in the public general community
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE group_id=1")
            data = dictfetchall(cursor)
            data = formatPosts(data)

            # Store posts in context dictionary
            context = {
                'data': data,
            }

        return render(request, 'index.html', context)

    # Apply filter is user is logged in and selects it.
    if request.POST.get("filter"):
        group_name = request.POST.get("group_select")

        # If filter not selected, display all users community posts
        if group_name=="query_all_groups":
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM posts")
                data = dictfetchall(cursor)
        else:
            # If user selects to filter, filter based on the community selected.
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM uni_groups WHERE group_name=%s", (str(group_name),))
                data = cursor.fetchone()
                group_id = data[0]

            # Get the posts from the selected group
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM posts WHERE group_id=%s", (str(group_id),))
                data = dictfetchall(cursor)  # putting it int a dict
    else:
        # If no filter selected display all posts from communities user is in
        with connection.cursor() as cursor:

            # Get ths users joined communities
            user = Users.objects.get(user_id=user_id)
            members = Members.objects.filter(user=user).values_list('group')
            group_list = []
            for i in members:
                group_list.append(i[0])

            # Get all the posts from the database
            cursor.execute("SELECT * FROM posts")
            data = dictfetchall(cursor)

        # Filter posts based on which ones belong to communities user is in.
        new_data = []
        for i in data:
            if i['group_id'] in group_list:
                new_data.append(i)

        data = new_data

    # Gather context data to display on template page
    data = formatPosts(data)
    groups = UniGroups.objects.all()
    pic_url = getProfile(request)
    user_id = request.session['user_id']
    context = {
        'data': data,
        'groups': groups,
        'user_id': user_id,
        'pfp': pic_url,
    }
    return render(request, 'index.html', context)


@csrf_exempt
def profile(request):
    """
    View to display the profile.html template.
    """

    # Access control - check user is logged in before displaying page
    try:
        user_id = request.session['user_id']
    except:
        return render(request, 'login.html')


    # If the user clicks the logout button, delete their session
    if request.POST.get("logout"):
        del request.session['user_id']
        return render(request, 'login.html')

    # If the user clicks the upload profile picture button, get the image.
    elif request.POST.get("uploadProfilePic"):
        image = request.FILES["image"]
        form = ProfilePicForm(request.POST, request.FILES)
        record = Pics(pic=image)
        record.save()

        # Save image reference in the pics table
        pic_id = record.pic_id
        user = Users.objects.get(user_id=user_id)
        user.pic_id = pic_id
        user.save()
    else:
        form = ProfilePicForm()

    # Get a list of the users joined communities
    user = Users.objects.get(user_id=user_id)
    members = Members.objects.filter(user=user).values_list('group')
    group_list = []
    for i in members:
        group_list.append(i[0])
    groups = UniGroups.objects.filter(group_id__in=group_list).values_list('group_name', 'fee', 'group_email')

    # Collect context to be displayed on the HTML template
    pic_url = getProfile(request)
    user_id = request.session['user_id']
    context = {'user': user, 'groups': groups, 'form': form,
               'user_id': user_id, 'pfp': pic_url, }

    return render(request, 'profile.html', context)


@csrf_exempt
def register(request):
    """
    View to display the register.html template.
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

    # Access control - check user is logged in before displaying page
    try:
        user_id = request.session['user_id']
    except:
        return render(request, 'login.html')

    # Get the user ID and their name
    user = Users.objects.get(user_id=user_id)
    post_owner = user.name

    if request.method == 'POST':
        # Check if an image was uploaded and get it if yes
        try:
            image = request.FILES['image']
        except:
            image = ""

        # Get data from HTML form
        post_name = request.POST['post_name']
        start = request.POST['start']
        end = request.POST['end']
        description = request.POST['description']
        attendees_min = request.POST['attendees_min']
        attendees_max = request.POST['attendees_max']
        location = request.POST['location']
        type = request.POST['type']
        group_id = request.POST['group']
        group = UniGroups.objects.get(group_id=group_id)

        # Check post achievement


        
        # Save the new post
        form = PostForm(request.POST, request.FILES, user_id=user_id)
        record = Posts(post_name=post_name, start=start, post_owner=post_owner, end=end,
                       description=description, attendees_min=attendees_min, group=group,
                       attendees_max=attendees_max, location=location, type=type,image=image)


        record.save()

        # Set post user_id to the users ID
        post_id = record.post_id
        with connection.cursor() as cursor:
            cursor.execute("UPDATE posts SET user_id=%s WHERE post_id=%s", (user_id, post_id,))
        id = record.post_id

        try:
            user = Users.objects.get(user=user)
        except:
            user = ""

        # If a post is an event store in attendees table
        if type == "event" and user != "":
            event = Posts.objects.get(post_id=id)
            attendee_record = Attendees(user=user, event=event)
            attendee_record.save()

        return redirect('/')

    else:
        form = PostForm(user_id=user_id)

    # Get all of users groups
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM uni_groups")
        data = dictfetchall(cursor)

    # Get context data to be displayed on the template
    pic_url = getProfile(request)
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

    # Access control - check user is logged in before displaying page
    try:
        user_id = request.session['user_id']
    except:
        return render(request, 'login.html')

    return render(request, 'creategroup.html')


def viewAllEvents(request):
    """
    View to display the showevents.html template.
    Passes the the context dictionary with data with events
    data to the template to be displayed
    """

    # Access control - check user is logged in before displaying page
    try:
        user_id = request.session['user_id']
    except:
        return render(request, 'login.html')

    # Select all the events from the events table
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM posts")
        data = dictfetchall(cursor)

    # Get context to be displayed in template
    pic_url = getProfile(request)
    context = {'data': data, 'user_id': user_id,
               'pfp': pic_url}

    return render(request, 'showevents.html', context)


def viewEventDetails(request, post_id):
    """
    View to display the event.html template.
    Passes the the context dictionary with data about the individual
    event to be displayed in the template.
    """

    # Access control - check user is logged in before displaying page
    try:
        user_id = request.session['user_id']
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
    """
    Function to get all the communities the user is in, and is not in
    """
    user = Users.objects.get(user_id=request.session['user_id'])
    user_id = str(user.user_id)

    # Get list of communities user is in
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM members WHERE user_id=%s", (user_id,) )
        data = cursor.fetchall()

    # Store them in a list of integers
    group_list = []
    for i in data:
        group_list.append(i[2])

    # Get communities user is not in
    groups = UniGroups.objects.all().exclude(group_id__in=group_list).values_list(
        'group_id', 'group_name', 'fee','group_email')

    # Get communities user is in
    in_groups = UniGroups.objects.filter(group_id__in=group_list).values_list(
        'group_id', 'group_name', 'fee','group_email')

    # Get context to display on template
    pic_url = getProfile(request)
    user_id = request.session['user_id']
    return {'outgroups': groups, 'ingroups': in_groups, 'user_id': user_id,
            'pfp': pic_url}


def viewGroups(request):
    """
    View to display the showgroups.html template.
    Passes the the context dictionary with data to be displayed.
    """
    # Access control - check user is logged in before displaying page
    try:
        user_id = request.session['user_id']
    except:
        return render(request, 'login.html')

    # Select all the events from the events table and save them into a dictionary,
    # pass to the showevents template

    context = getViewGroupsData(request)
    return render(request, 'showgroups.html', context)


def joinGroup(request, group_id):
    """
    Function to add a user to a community
    """
    # Get group and user, add them to the members table
    group = UniGroups.objects.get(group_id=group_id)
    user = Users.objects.get(user_id=request.session['user_id'])
    member_record = Members(user=user, group=group, is_group_admin=0)
    member_record.save()
    context = getViewGroupsData(request)
    return render(request, 'showgroups.html', context)


def leaveGroup(request, group_id):
    """
    Function to remove a user from a community
    """
    # Get the community and the user objects
    group = UniGroups.objects.get(group_id=group_id)
    user = Users.objects.get(user_id=request.session['user_id'])

    # Remove user from community
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
    # Get the user ID
    user_id = request.session['user_id']

    with connection.cursor() as cursor:
        #Get all achievements from achievements table
        cursor.execute("SELECT * from achievements")
        achievement = dictfetchall(cursor)

        # Check if user has earnt achievement
        for i in achievement:
            requirement = i["requirement"]
            cursor.execute("SELECT * FROM has_ach WHERE ach_id = %s AND user_id = %s",
                           (i["ach_id"],user_id,))

            ach_has = cursor.fetchone()

            # If they do not have achievement, check if they have achieved it
            if not ach_has:
                # Run the verification code to see if they have achieved achievement
                exec(requirement)
                ach_get = cursor.fetchone()

                if ach_get:
                    # Give user achievement if they have earnt it
                    ach_id = i["ach_id"]
                    ach_id = str(ach_id)
                    cursor.execute("INSERT INTO has_ach(ach_id, user_id) VALUES (%s,%s)",
                                   (ach_id,user_id,))

        # Get user achievements to display in table
        cursor.execute("SELECT * FROM has_ach JOIN achievements "
                       "ON has_ach.ach_id = achievements.ach_id "
                       "WHERE user_id = %s", (user_id,))
        user_achs = dictfetchall(cursor)
        pic_url = getProfile(request)
        context = {'data': user_achs, 'user_id': user_id,
                   'pfp': pic_url}

    return render(request, 'showachs.html', context)

def termsConditions(request):
    """
    View to display the termsconditions.html template.
    """
    return render(request, 'termsconditions.html')

# Define functions

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

    # Concatenate first and last name
    fullName = fname + " " + name

    # Generate salt
    salt = ''.join([random.choice(string.ascii_letters) for i in range(16)])
    salted_password = salt + password

    # Hash the password
    hash_sha3_512 = hashlib.new("sha3_512", salted_password.encode())
    pswd = hash_sha3_512.digest()

    pic = Pics(pic="static/exehubapp/pfp/default.png")
    pic.save()
    pic_id = pic.pic_id

    # Save new user to the Model.
    record = Users(is_server_admin=False, date_of_birth=dob, email=email,
                   name=fullName, password_hash=pswd, salt=salt, pic_id=pic_id)

    record.save()

    # Map user to community
    group = UniGroups.objects.get(group_id=1)
    member_record = Members(user=record, group=group, is_group_admin=0)
    member_record.save()

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

    record.save()

    # Map user to community
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
    View to show the leaderboard.html view
    """

    # Access control - check user is logged in
    try:
        user_id = request.session['user_id']
    except:
        return render(request, 'login.html')

    # Get the total points of each user
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, SUM(value) AS sum FROM has_ach JOIN achievements "
                       "ON has_ach.ach_id = achievements.ach_id JOIN users "
                       "ON has_ach.user_id = users.user_id "
                       "GROUP BY users.user_id ORDER BY sum DESC")
        data = dictfetchall(cursor)

    #
    pic_url = getProfile(request)
    user_id = request.session['user_id']
    context= {'data': data,'user_id': user_id,
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


    # Remove all of users posts before deletion of account
    posts = Posts.objects.filter(user_id=request.session['user_id'])
    for i in posts:
        children = Posts.objects.filter(parent=i.post_id)
        for j in children:
            j.delete()
        i.delete()

    # If user deleted successfully, return 0
    user.delete()
    del request.session['user_id']
    return HttpResponse(0)


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
        upvote_num = upvote_num - 1
        print("Changing upvote by -1")
        context = {'votes': upvote_num,
                   'change': -1
                   }
        return HttpResponse(json.dumps(context), content_type='application/json')

    else:
        # user has not upvoted
        print("User has not upvoted yet")
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(user_id) FROM upvotes WHERE post_id = %s", (post_id,))
            data = cursor.fetchall()
            print(data)
            upvote_num = data[0][0]
            cursor.execute("INSERT INTO upvotes VALUES (%s, %s)", (user_id, post_id))
        upvote_num = upvote_num + 1
        print("Changing upvote by + 1")
        context= {'votes': upvote_num,
                  'change': 1
                  }
        return HttpResponse(json.dumps(context), content_type='application/json')

        # If update successful, return 0
        # If update unsuccessful, return 1
        print("Fail")
        context = {'votes': -1,
                   'change': 0
                   }
        return HttpResponse(json.dumps(context), content_type='application/json')


def getProfile(request):
    """
    Function to get the image URL of the users profile picture.
    """
    # Get the user ID, retrieve their object from the model, and get the image path
    user_id = request.session['user_id']
    pic_id = Users.objects.get(user_id=user_id).pic_id
    pic_url = Pics.objects.get(pic_id=pic_id).pic
    return pic_url


def formatPosts(data):
    """
    Function to get the profile picture of posts owner
    """

    # Loop through each post and get the posters profile picture.
    for row in data:
        user_id = row['user_id']
        pic_id = Users.objects.get(user_id=user_id).pic_id
        pic_url = Pics.objects.get(pic_id=pic_id).pic
        row['poster_pfp'] = pic_url

    return data

