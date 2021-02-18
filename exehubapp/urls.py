from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addevent/', views.addEvent, name='addevent'),
    path('addevent/create/', views.createEvent, name='createEvent'),
    path('events/', views.viewAllEvents, name='events'),
    path('events/<int:event_id>', views.viewEventDetails, name='event'),
    path('creategroup/', views.createGroup, name='creategroup'),

]
