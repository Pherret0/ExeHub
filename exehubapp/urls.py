from django.urls import path

from exehubapp import views

# Specify URL patterns for each view in the web page.

urlpatterns = [

    # URL Patterns
    path('', views.index, name='index'),
    path('cat/', views.cat, name='cat'),
    path('events/<int:post_id>', views.viewEventDetails, name='event'),
    path('termsconditions/', views.termsConditions, name='termsConditions'),

    # Group URL Patterns
    path('creategroup/', views.createGroup, name='createGroup'),
    path('creategroup/create/', views.createGroupForm, name='createGroupForm'),
    path('creategroup/verifyunique/', views.verifyUniqueGroup, name='verifyUniqueGroup'),
    path('groups/', views.viewGroups, name='groups'),

    # Register URL Patterns
    path('register/', views.register, name='register'),
    path('register/addUser/', views.addUser, name='addUser'),
    path('register/verifyuniqueemail/', views.verifyUniqueEmail, name='verifyuniqueemail'),

    # Login URL Patterns
    path('login/', views.login, name='login'),
    path('login/validateLogin/', views.validateLogin, name='validateLogin'),

    # Post URL Patterns
    path('addevent/', views.addEvent, name='addevent'),
    path('events/', views.viewAllEvents, name='events'),

    # Profile URL Patterns
    path('profile/', views.profile, name='profile'),
    path('profile/updateemail/', views.updateEmail, name='updateEmail'),
    path('profile/updatepassword/', views.updatePassword, name='updatePassword'),
    path('profile/verifyuniqueemail/', views.verifyUniqueEmail, name='verifyuniqueemail'),
    path('profile/deleteaccount/', views.deleteAccount, name='deleteAccount'),

    #Achievements URL Patterns
    path('achievements/', views.viewAchs, name='achievements'),
]
