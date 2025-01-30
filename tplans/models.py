from django.db import models
from django.conf import settings

class WorkoutPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    goal = models.CharField(max_length=100, choices=[
        ('Muskelaufbau', 'Muskelaufbau'),
        ('Kraftausdauer', 'Kraftausdauer'),
        ('Gewichtsverlust', 'Gewichtsverlust'),
    ])
    experience_level = models.CharField(max_length=100, choices=[
        ('Anfänger', 'Anfänger'),
        ('Fortgeschritten', 'Fortgeschritten'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.name}"

class WorkoutExercise(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name="exercises")
    exercise_name = models.CharField(max_length=255)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.workout_plan.name} - {self.exercise_name}"
