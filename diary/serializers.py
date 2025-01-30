from rest_framework import serializers
from .models import DiaryEntry, WorkoutPlan, WorkoutExercise

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = ["id", "exercise_name", "sets", "reps", "rest_time"]

class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True)

    class Meta:
        model = WorkoutPlan
        fields = ["id", "name", "goal", "experience_level", "exercises"]

class DiaryEntrySerializer(serializers.ModelSerializer):
    workout_plan = WorkoutPlanSerializer()

    class Meta:
        model = DiaryEntry
        fields = ["id", "date", "workout_plan", "completed_exercises"]
