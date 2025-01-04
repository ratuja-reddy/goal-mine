from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-goal/', views.add_goal, name='add_goal'),
    path('add-habit-log/', views.add_habit_log, name='add_habit_log'),
]
