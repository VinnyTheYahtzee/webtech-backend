# exercises/models.py

from django.db import models

class Exercise(models.Model):
    MUSCLE_GROUPS = [
        ('chest', 'Brust'),
        ('back', 'Rücken'),
        ('legs', 'Beine'),
        ('shoulders', 'Schultern'),
        ('arms', 'Arme'),
        ('abs', 'Bauch'),
        # Add or change as needed
    ]

    name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=50, choices=MUSCLE_GROUPS)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=50, blank=True)  # e.g., "Beginner", "Intermediate", etc.
    tier = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_muscle_group_display()})"
