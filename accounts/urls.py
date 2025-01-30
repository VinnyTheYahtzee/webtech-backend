from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    UserRegistrationView,
    UserLoginView,
    LogoutView,
    ChangePasswordView,
    DeleteAccountView,
    AdminUserListView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', AdminUserListView.as_view(), name='admin_user_list'),

    # Single route for the current user's profile: GET, PUT, PATCH
    path('profile/', UserProfileViewSet.as_view({
       'get': 'retrieve',
       'put': 'update',
       'patch': 'partial_update',
    }), name='user-profile'),

    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
]

# Optionally, a function-based logout if you want:
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # logout logic
    return Response(status=status.HTTP_200_OK)
