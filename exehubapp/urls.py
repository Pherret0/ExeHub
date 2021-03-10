from django.urls import path
from exehubapp import views

# Specify URL patterns for each view in the web page.

urlpatterns = [

    # URL Patterns
    path('', views.index, name='index'),
    path('events/<int:post_id>', views.viewEventDetails, name='event'),
    path('termsconditions/', views.termsConditions, name='termsConditions'),
    path('upvote/', views.upvote, name='upvote'),

    # Groups URL Patterns
    path('groups/', views.viewGroups, name='groups'),
    path('groups/create/', views.createGroupForm, name='createGroupForm'),
    path('groups/verifyunique/', views.verifyUniqueGroup, name='verifyUniqueGroup'),
    path('groups/join/<int:group_id>', views.joinGroup, name='joinGroup'),
    path('groups/delete/<int:group_id>', views.leaveGroup, name='leaveGroup'),

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
    path('post/<int:post_id>', views.post, name='post'),
    path('post/comment/', views.comment, name='comment'),

    # Profile URL Patterns
    path('profile/', views.profile, name='profile'),
    path('profile/updateemail/', views.updateEmail, name='updateEmail'),
    path('profile/updatepassword/', views.updatePassword, name='updatePassword'),
    path('profile/verifyuniqueemail/', views.verifyUniqueEmail, name='verifyuniqueemail'),
    path('profile/deleteaccount/', views.deleteAccount, name='deleteAccount'),

    #Achievements URL Patterns
    path('achievements/', views.viewAchs, name='achievements'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
