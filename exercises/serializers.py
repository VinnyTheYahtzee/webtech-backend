from rest_framework import serializers
from .models import Exercise

class ExerciseSerializer(serializers.ModelSerializer):
    muscle_group_display = serializers.CharField(source='get_muscle_group_display', read_only=True)

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'muscle_group', 'muscle_group_display', 'description', 'difficulty']
