from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class HabitLog(models.Model):
    goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    date = models.DateField()
    achieved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('goal', 'date')  # Ensure no duplicate entries for the same goal and date

    def save(self, *args, **kwargs):
        # Check if a record for the same goal and date already exists
        existing_log = HabitLog.objects.filter(goal=self.goal, date=self.date).first()
        if existing_log:
            # Update the existing record
            existing_log.achieved = self.achieved
            existing_log.save()
        else:
            # No record exists, create a new one
            super().save(*args, **kwargs)