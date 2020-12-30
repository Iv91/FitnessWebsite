from django.contrib import admin
from .models import Category, Exercise, Member, Workout
# Register your models here.

admin.site.register(Category)
admin.site.register(Exercise)
admin.site.register(Member)
admin.site.register(Workout)
