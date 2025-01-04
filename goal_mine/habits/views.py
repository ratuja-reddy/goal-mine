from django.shortcuts import render, redirect
from .models import Goal, HabitLog
from .forms import GoalForm, HabitLogForm
from calendar import monthrange
from datetime import datetime

def dashboard(request):
    # Get selected month and year, default to current
    month = int(request.GET.get('month', datetime.now().month))
    year = int(request.GET.get('year', datetime.now().year))

    # Ensure valid year and month
    if not (1 <= month <= 12):
        month = datetime.now().month
    if year < 2025:
        year = 2025

    user_goals = Goal.objects.filter(user=request.user)
    logs = HabitLog.objects.filter(goal__user=request.user, date__year=year, date__month=month)

    # Generate calendar data
    days_in_month = monthrange(year, month)[1]
    calendar_data = []
    for day in range(1, days_in_month + 1):
        day_logs = logs.filter(date__day=day)
        if not day_logs.exists():
            color = "grey"
            tooltip = "No habits logged"
        elif all(log.achieved for log in day_logs):
            color = "green"
            tooltip = ", ".join([f"{log.goal.name} (Achieved)" for log in day_logs])
        elif any(log.achieved for log in day_logs):
            color = "orange"
            tooltip = ", ".join([
                f"{log.goal.name} ({'Achieved' if log.achieved else 'Not Achieved'})"
                for log in day_logs
            ])
        else:
            color = "red"
            tooltip = ", ".join([f"{log.goal.name} (Not Achieved)" for log in day_logs])
        calendar_data.append({"day": day, "color": color, "tooltip": tooltip})

    # Calculate streaks
    streaks = {
        goal.name.upper(): logs.filter(goal=goal, achieved=True).count() for goal in user_goals
    }

    return render(request, 'habits/dashboard.html', {
        'calendar_data': calendar_data,
        'streaks': streaks,
        'goals': user_goals,
        'month': month,
        'year': year,
    })

def add_goal(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('dashboard')
    else:
        form = GoalForm()
    return render(request, 'habits/add_goal.html', {'form': form})

def add_habit_log(request):
    if request.method == "POST":
        form = HabitLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = HabitLogForm()
    return render(request, 'habits/add_habit_log.html', {'form': form})