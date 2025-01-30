from django.urls import path
from .views import WorkoutPlanViewSet


urlpatterns = [
    path('', WorkoutPlanViewSet.as_view({'get': 'list', 'post': 'create'}), name='workout-plan-list'),
]
