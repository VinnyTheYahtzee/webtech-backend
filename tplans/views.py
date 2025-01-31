from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import WorkoutPlan, WorkoutExercise
from rest_framework.decorators import action
from .serializers import WorkoutPlanSerializer
import logging
from django.db import transaction

logger = logging.getLogger(__name__)  # ✅ Add logging

class WorkoutPlanPagination(PageNumberPagination):  # ✅ Pagination
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling Workout Plans.
    Users can Create, Retrieve, Update, and Delete their own workout plans.
    """
    serializer_class = WorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = WorkoutPlanPagination

    def get_queryset(self):
        """
        Ensure users can only see their own workout plans.
        """
        return WorkoutPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Attach the authenticated user to the workout plan before saving.
        """
        try:
            serializer.save(user=self.request.user)
            logger.info(f"WorkoutPlan created by {self.request.user.email}")
        except Exception as e:
            logger.error(f"Error creating WorkoutPlan: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """
        Generate a default workout plan based on user input.
        """
        experience = request.data.get("experience_level", "Anfänger")
        goal = request.data.get("goal", "Muskelaufbau")

        with transaction.atomic():
            workout_plan = WorkoutPlan.objects.create(
                user=request.user,
                name=f"{goal} - {experience}",
                goal=goal,
                experience_level=experience
            )

            # ✅ Add Default Exercises to the Plan
            default_exercises = [
                {"exercise_name": "Bankdrücken", "sets": 3, "reps": 12},
                {"exercise_name": "Kniebeugen", "sets": 3, "reps": 10},
                {"exercise_name": "Klimmzüge", "sets": 3, "reps": 8},
            ]

            for ex in default_exercises:
                WorkoutExercise.objects.create(workout_plan=workout_plan, **ex)

        # ✅ Serialize the workout plan **with** exercises
        response_data = WorkoutPlanSerializer(workout_plan).data

        logger.info(f"Generated workout plan '{workout_plan.name}' for {request.user.email}")
        return Response(response_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        Override delete method to ensure only owners can delete.
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"error": "You can only delete your own plans."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response({"message": "Workout plan deleted successfully."}, status=status.HTTP_204_NO_CONTENT)