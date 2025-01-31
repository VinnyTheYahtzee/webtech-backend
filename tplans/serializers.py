# serializers.py
from rest_framework import serializers
from .models import WorkoutPlan, WorkoutExercise, Exercise

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'muscle_group', 'equipment']

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ['id', 'exercise', 'sets', 'reps', 'rest']

class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'name', 'goal', 'experience_level', 'created_at', 'exercises']
