from django.contrib import admin

# Register your models here.
from .models import Goal, Race, Training, Photo

admin.site.register(Race)
admin.site.register(Training)
admin.site.register(Goal)
admin.site.register(Photo)