from django.db import models

class Achievements(models.Model):
    ach_id = models.AutoField(unique=True, primary_key=True)
    ach_name = models.CharField(max_length=64)
    requirement = models.TextField()
    value = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'achievements'


class Attendees(models.Model):
    attendee_id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    event = models.ForeignKey('Posts', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'attendees'
        unique_together = (('user', 'event'),)


class Members(models.Model):
    member_id = models.AutoField(primary_key = True, unique=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    group = models.ForeignKey('UniGroups', models.DO_NOTHING)
    is_group_admin = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'members'
        unique_together = (('user', 'group'),)

    def __str__(self):
        return self.group.group_name


class Pics(models.Model):
    pic_id = models.AutoField(primary_key=True)
    pic = models.FileField(upload_to="static/exehub/pfp")

    class Meta:
        managed = False
        db_table = 'pics'


class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_name = models.CharField(max_length=50)
    post_owner = models.CharField(max_length=747)
    group = models.ForeignKey('UniGroups', models.DO_NOTHING)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    attendees_min = models.PositiveSmallIntegerField(blank=True, null=True)
    attendees_max = models.PositiveSmallIntegerField(blank=True, null=True)
    type = models.CharField(max_length=7)
    image = models.FileField(blank=True, null=True, upload_to="static/exehubapp/post_images")
    parent = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'


class Products(models.Model):
    prod_id = models.AutoField(unique=True, primary_key=True)
    prod_name = models.CharField(max_length=64)
    prod_desc = models.CharField(max_length=1024)
    cost = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class UniGroups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(unique=True, max_length=50)
    group_owner = models.CharField(max_length=747, blank=True, null=True)
    group_irc = models.CharField(unique=True, max_length=200, blank=True, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    group_email = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = 'uni_groups'

    def __str__(self):
        return self.group_name

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    is_server_admin = models.PositiveIntegerField()
    date_of_birth = models.DateField()
    email = models.CharField(unique=True, max_length=254)
    irc_username = models.CharField(max_length=9, blank=True, null=True)
    password_hash = models.BinaryField(max_length=64)
    name = models.CharField(max_length=747)
    salt = models.CharField(max_length=16)
    pic = models.ForeignKey(Pics, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Upvotes(models.Model):
    user_id = models.ForeignKey('Users', models.DO_NOTHING)
    post_id = models.ForeignKey('Posts', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'upvotes'

