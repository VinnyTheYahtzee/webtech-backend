# exercises/views.py

from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from .models import Exercise
from .serializers import ExerciseSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions

class ExerciseListView(generics.ListAPIView):
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all().order_by('muscle_group', 'name')

    def get_queryset(self):
        qs = super().get_queryset()

        # Optional: filter by muscle group or search
        muscle = self.request.query_params.get('muscle')
        search = self.request.query_params.get('search')

        if muscle:
            qs = qs.filter(muscle_group=muscle)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return qs

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])  # Only admins can add exercises
def populate_exercises(request):
    exercises = [
        {"name": "Bankdrücken", "muscle_group": "chest", "description": "Klassische Brustübung mit der Langhantel auf der Bank.", "difficulty": "Intermediate", "tier": "A"},
        {"name": "Schrägbankdrücken positiv", "muscle_group": "chest", "description": "Wird auf einer schrägen Bank ausgeführt mit einer positiven Steigung, um die obere Brust zu treffen.", "difficulty": "Intermediate", "tier": "S"},
        {"name": "Schrägbankdrücken negativ", "muscle_group": "chest", "description": "Wird auf einer schrägen Bank ausgeführt mit einer negativen Steigung, um die untere Brust zu treffen. Wird nur gebraucht, wenn man in dem Bereich Defizite hat.", "difficulty": "Intermediate", "tier": "B"},
        {"name": "Klimmzüge", "muscle_group": "back", "description": "Eine der besten Übungen für den Latismus. Ohne Gewicht A-Tier, mit Gewicht S-Tier", "difficulty": "Intermediate", "tier": "A"},
        {"name": "Latziehen", "muscle_group": "back", "description": "Alternativ zu Klimmzügen, besonders für Anfänger geeignet.", "difficulty": "Beginner", "tier": "B"},
        {"name": "Kreuzheben", "muscle_group": "legs", "description": "Grundübung für den unteren Rücken, den Gluteus und die Oberschenkel.", "difficulty": "Intermediate", "tier": "A"},
        {"name": "Kniebeugen", "muscle_group": "legs", "description": "Grundübung für die Beine mit der Langhantel.", "difficulty": "Intermediate", "tier": "A"},
        {"name": "Beinpresse", "muscle_group": "legs", "description": "Alternativ zu Kniebeugen, trainiert Quadrizeps und Gesäßmuskulatur. Je nach Gerät S bis B-Tier", "difficulty": "Beginner", "tier": "A"},
        {"name": "Schulterdrücken", "muscle_group": "shoulders", "description": "Drückbewegung über den Kopf für die Schulter.", "difficulty": "Intermediate", "tier": "A"},
        {"name": "Seitheben", "muscle_group": "shoulders", "description": "Isolation für die seitlichen Schultern.", "difficulty": "Beginner", "tier": "B"},
        {"name": "Bizepscurls", "muscle_group": "arms", "description": "Klassische Übung für den Bizeps mit Kurzhanteln.", "difficulty": "Beginner", "tier": "B"},
        {"name": "Trizepsdrücken", "muscle_group": "arms", "description": "Trainiert den Trizeps mit Kabelzug oder Hantel.", "difficulty": "Beginner", "tier": "B"},
        {"name": "Sit-ups", "muscle_group": "abs", "description": "Beliebte Bauchmuskelübung.", "difficulty": "Beginner", "tier": "C"},
        {"name": "Planks", "muscle_group": "abs", "description": "Isometrische Übung für den gesamten Rumpf.", "difficulty": "Intermediate", "tier": "B"}
    ]

    created_exercises = []
    for exercise_data in exercises:
        exercise, created = Exercise.objects.get_or_create(name=exercise_data['name'], defaults=exercise_data)
        if created:
            created_exercises.append(exercise_data)

    return Response({"message": f"{len(created_exercises)} neue Übungen hinzugefügt."}, status=status.HTTP_201_CREATED)
