from django.contrib import admin

from .models import ExehubappEvent
from .models import ExehubappGroup
from .models import ExehubappUser
from .models import ExehubappAttendee
from .models import ExehubappMember
admin.site.register(ExehubappEvent)
admin.site.register(ExehubappGroup)
admin.site.register(ExehubappUser)
admin.site.register(ExehubappAttendee)
admin.site.register(ExehubappMember)