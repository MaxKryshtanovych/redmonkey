from django.contrib import admin
from .models import Client, Check, Employer, Course

admin.site.register(Client)
admin.site.register(Check)
admin.site.register(Employer)
admin.site.register(Course)
