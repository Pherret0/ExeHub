from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addevent/', views.addEvent, name='addevent'),
    path('addevent/create/', views.createEvent, name='createEvent'),
    path('events/', views.viewEvents, name='events'),

]