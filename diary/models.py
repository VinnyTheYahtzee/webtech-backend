from django.db import models
from django.conf import settings

class WorkoutPlan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diary_workout_plans",  # 👈 Add this
    )
    name = models.CharField(max_length=255)
    goal = models.CharField(max_length=255)
    experience_level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class WorkoutExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name="exercises")
    exercise_name = models.CharField(max_length=255)
    sets = models.IntegerField(default=3)
    reps = models.IntegerField(default=10)
    rest_time = models.IntegerField(default=90)  # Default rest time

class DiaryEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    completed_exercises = models.JSONField(default=list)  # Stores per-exercise sets, reps, rest

    def __str__(self):
        return f"{self.user.email} - {self.date} - {self.workout_plan.name}"
