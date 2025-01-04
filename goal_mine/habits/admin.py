from django.contrib import admin
from .models import Goal, HabitLog

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')  # Customize what fields to show in the admin list view
    search_fields = ('name',)  # Add a search box for goal names

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('goal', 'date', 'achieved')  # Customize what fields to show
    list_filter = ('achieved', 'date')  # Add filters for achieved status and date
    search_fields = ('goal__name',)  # Search by goal name
