from django.urls import path

from . import views

# Specify URL patterns for each view in the web page.

urlpatterns = [
    path('', views.index, name='index'),
    path('addevent/', views.addEvent, name='addevent'),
    path('addevent/create/', views.createEvent, name='createEvent'),
    path('events/', views.viewAllEvents, name='events'),
    path('cat/', views.cat, name='cat'),
    path('events/<int:event_id>', views.viewEventDetails, name='event'),
    path('creategroup/', views.createGroup, name='createGroup'),
    path('creategroup/create/', views.createGroupForm, name='createGroupForm'),
    path('creategroup/verifyunique/', views.verifyUniqueGroup, name='verifyUniqueGroup'),
    path('register/', views.register, name='register'),
    path('register/addUser/', views.addUser, name='addUser'),
    path('register/verifyuniqueemail/', views.verifyUniqueEmail, name='verifyuniqueemail'),
    path('groups/', views.viewGroups, name='groups'),
    path('termsconditions/', views.termsConditions, name='termsConditions'),
    path('profile/', views.profile, name='profile'),
    path('profile/updateemail/', views.updateEmail, name='updateEmail'),
    path('profile/updatepassword/', views.updatePassword, name='updatePassword'),
    path('profile/verifyuniqueemail/', views.verifyUniqueEmail, name='verifyuniqueemail'),
    path('profile/deleteaccount/', views.deleteAccount, name='deleteAccount'),


]
