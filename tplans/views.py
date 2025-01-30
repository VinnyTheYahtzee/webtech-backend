from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import WorkoutPlan
from .serializers import WorkoutPlanSerializer
import logging

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
    pagination_class = WorkoutPlanPagination  # ✅ Pagination

    def get_queryset(self):
        """
        Ensure users can only see their own workout plans.
        """
        user = self.request.user
        return WorkoutPlan.objects.filter(user=user)

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

    def list(self, request, *args, **kwargs):
        """
        Handle GET requests to list user's workout plans.
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Override delete method to ensure only owners can delete.
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"error": "You can only delete your own plans."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response({"message": "Workout plan deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
