from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from .models import Exercise
from .serializers import ExerciseSerializer

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
