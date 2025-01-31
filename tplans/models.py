# tplans/models.py

from django.db import models
from django.conf import settings  # Import settings to access AUTH_USER_MODEL

class WorkoutPlan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the custom user model
        on_delete=models.CASCADE,
        related_name='workout_plans'  # Optional: Allows reverse lookup from user to plans
    )
    name = models.CharField(max_length=100)
    goal = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class WorkoutExercise(models.Model):
    workout_plan = models.ForeignKey(
        'WorkoutPlan',
        on_delete=models.CASCADE,
        related_name='exercises'
    )
    exercise = models.ForeignKey(
        'exercises.Exercise',  # Reference the Exercise model from exercises app
        on_delete=models.CASCADE,
        null=True,             # Allow nulls temporarily
        blank=True             # Allow blank in forms
    )
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    rest = models.PositiveIntegerField(default=60)  # Rest time in seconds
    
    def __str__(self):
        return f"{self.exercise.name if self.exercise else 'No Exercise'} - {self.sets}x{self.reps}"
