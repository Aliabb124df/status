from django.contrib import admin
from .models import Person,TaskPerson,Marrid,Dead,Widower,Divorce
from django.contrib.auth.models import User

admin.site.register(Person)
admin.site.register(TaskPerson)
admin.site.register(Marrid)
admin.site.register(Dead)
admin.site.register(Widower)
admin.site.register(Divorce)
#admin.site.register()