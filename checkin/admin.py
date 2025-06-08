from django.contrib import admin
from .models import Room, CheckIn,Bill

admin.site.register(Bill)
admin.site.register(Room)
admin.site.register(CheckIn)
