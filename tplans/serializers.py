# tplans/serializers.py

from rest_framework import serializers
from .models import WorkoutPlan, WorkoutExercise
from exercises.serializers import ExerciseSerializer  # Correct path

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)
    
    class Meta:
        model = WorkoutExercise
        fields = ['id', 'exercise', 'sets', 'reps', 'rest']

class WorkoutPlanSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Or use a dedicated UserSerializer
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)
    
    class Meta:
        model = WorkoutPlan
        fields = ['id', 'user', 'name', 'goal', 'experience_level', 'created_at', 'exercises']
