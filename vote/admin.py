from django.contrib import admin
from vote.models import *

admin.site.register(Poll)
admin.site.register(Status)
admin.site.register(Team)
admin.site.register(Vote)
