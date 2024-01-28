from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *

admin.site.register(Events)
admin.site.register(Places)
admin.site.unregister(Group)
