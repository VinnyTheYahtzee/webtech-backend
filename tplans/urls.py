# tplans/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutPlanViewSet

router = DefaultRouter()
router.register(r'', WorkoutPlanViewSet, basename='workoutplan')

urlpatterns = [
    path('', include(router.urls)),
]
