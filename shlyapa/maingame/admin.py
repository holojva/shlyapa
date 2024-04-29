from django.contrib import admin
from .models import Rooms, Words, UpdatedUserModel
# Register your models here.
admin.site.register(Rooms)
admin.site.register(Words)
admin.site.register(UpdatedUserModel)