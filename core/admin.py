from django.contrib import admin
from .models import Habit, Progress


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    # Displayed columns
    list_display = ['id', 'user', 'name', 'slug', 'description']
    # Column filters
    list_filter = ['user']
    # Editable fields
    fields = ['id', 'user', 'name', 'slug', 'description']
    # Prepopulate slug field based on name
    prepopulated_fields = {'slug': ('name',)}
    # Order habits by user then name by default
    ordering = ['user', 'name']


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    # Displayed columns
    list_display = ['id', 'habit', 'date', 'completed']
    # Column filters
    list_filter = ['habit', 'date', 'completed']
