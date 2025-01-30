from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutPlanViewSet

router = DefaultRouter()
router.register(r'workout_plans', WorkoutPlanViewSet, basename='workout_plan')

urlpatterns = [
    path('', include(router.urls)),
]
