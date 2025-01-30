from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import DiaryEntry
from .serializers import DiaryEntrySerializer
from rest_framework.decorators import action

class DiaryEntryViewSet(viewsets.ModelViewSet):
    serializer_class = DiaryEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["GET"], url_path="by-date")
    def get_by_date(self, request):
        date = request.query_params.get("date")
        if not date:
            return Response({"error": "Date parameter is required"}, status=400)
        entries = DiaryEntry.objects.filter(user=request.user, date=date)
        return Response(DiaryEntrySerializer(entries, many=True).data)
