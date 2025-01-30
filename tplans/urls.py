from django.urls import path
from .views import WorkoutPlanViewSet

urlpatterns = [
    # List and Create Workout Plans
    path('', WorkoutPlanViewSet.as_view({'get': 'list', 'post': 'create'}), name='workout-plan-list'),

    # New: Explicit route for generating workout plans
    path('generate/', WorkoutPlanViewSet.as_view({'post': 'generate'}), name='workout-plan-generate'),
]
