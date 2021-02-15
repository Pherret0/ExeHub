from django.db import models

# Create your models here.
class Group(models.Model):
    group_name = models.CharField(max_length = 45)
    group_owner = models.CharField(max_length = 45)
    group_email = models.CharField(max_length = 45)
    group_irc = models.CharField(max_length = 45)
    fee = models.FloatField()
class Event(models.Model):
    name = models.CharField(max_length = 45)
    owner = models.CharField(max_length = 45)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    set_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    location = models.CharField(max_length = 45)
    description = models.CharField(max_length = 600)
    min_attendees = models.IntegerField()
    max_attendees = models.IntegerField()
class User(models.Model):
    is_server_admin = models.BooleanField()
    dob = models.DateField()
    email = models.CharField(max_length = 45)
    irc_user = models.CharField(max_length = 45)
    hashed_password = models.BinaryField(64)
class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_group_admin = models.BooleanField()
