from django.contrib import admin
from .models import Event
from .models import Group
from .models import User
from .models import Attendee
from .models import Member
admin.site.register(Event)
admin.site.register(Group)
admin.site.register(User)
admin.site.register(Attendee)
admin.site.register(Member)
