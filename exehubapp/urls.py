from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addevent/', views.addEvent, name='addevent'),
    path('addevent/create/', views.createEvent, name='createEvent'),
    path('events/', views.viewAllEvents, name='events'),
    path('cat/', views.cat, name='cat'),
    path('events/<int:event_id>', views.viewEventDetails, name='event'),
    path('creategroup/', views.createGroup, name='creategroup'),
    path('register/', views.register, name='register'),
    path('register/addUser/', views.addUser, name='addUser'),
    path('login/', views.login, name='login'),
    path('login/verifyUser/', views.verifyUser, name='verifyUser'),

]
