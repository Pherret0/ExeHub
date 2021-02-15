from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length = 45)
    owner = models.CharField(max_length = 45)
    #group_id = models.ForeignKey(Groups)
    set_date_time = models.DateField()
    end_date_time = models.DateField()
    location = models.CharField(max_length = 45)
    description = models.CharField(max_length = 500)
    min_attendees = models.IntegerField()
    max_attendees = models.IntegerField()
"""class Attendees(models.Model):
class Users(models.Model):
class Members(models.Model):
class Groups(models.Model):"""
