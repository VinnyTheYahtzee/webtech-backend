# exercises/urls.py
from django.urls import path
from .views import ExerciseListView, populate_exercises

urlpatterns = [
    path('', ExerciseListView.as_view(), name='exercise-list'),
    path('populate-exercises/', populate_exercises, name='populate-exercises'),
]
