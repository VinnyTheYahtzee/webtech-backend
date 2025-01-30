from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiaryEntryViewSet

router = DefaultRouter()
router.register(r"diary_entries", DiaryEntryViewSet, basename="diary_entry")

urlpatterns = [
    path("", include(router.urls)),
]
