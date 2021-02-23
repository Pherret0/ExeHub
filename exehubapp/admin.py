from django.contrib import admin

from .models import Events
from .models import UniGroups
from .models import Users
from .models import Attendees
from .models import Members
admin.site.register(Events)
admin.site.register(UniGroups)
admin.site.register(Users)
admin.site.register(Attendees)
admin.site.register(Members)

