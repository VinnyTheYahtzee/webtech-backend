from rest_framework import serializers
from .models import WorkoutPlan, WorkoutExercise

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = ['id', 'exercise_name', 'sets', 'reps']

class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'name', 'goal', 'experience_level', 'created_at', 'exercises']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        workout_plan = WorkoutPlan.objects.create(**validated_data)
        
        for exercise_data in exercises_data:
            WorkoutExercise.objects.create(workout_plan=workout_plan, **exercise_data)

        return workout_plan
