from django.contrib import admin

from .models import Topic, Entry, Profile

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Profile)
# Register your models here.
