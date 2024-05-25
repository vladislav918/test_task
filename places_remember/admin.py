from django.contrib import admin
from .models import CustomUser, Memory, Coordinates


admin.site.register(CustomUser)

admin.site.register(Memory)

admin.site.register(Coordinates)
