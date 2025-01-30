from django.shortcuts import get_object_or_404
from numpy import generic
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile
from .serializers import UserProfileSerializer, UserRegistrationSerializer, AdminUserListSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


User = get_user_model()

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # If you want to show only the user's own profile in a list
        # return UserProfile.objects.filter(user=self.request.user)
        return UserProfile.objects.all()

    def get_object(self):
        # Retrieve the one UserProfile that matches the request.user
        return get_object_or_404(UserProfile, user=self.request.user)

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # Allow access without authentication

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Delete the token for the authenticated user
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
    
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

User = get_user_model()

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password2 = request.data.get('new_password2')

        if not old_password or not new_password or not new_password2:
            return Response({"detail": "Alle Felder müssen ausgefüllt sein."}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(old_password, user.password):
            return Response({"detail": "Altes Passwort ist falsch."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != new_password2:
            return Response({"detail": "Passwörter stimmen nicht überein."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        
        return Response({"detail": "Passwort erfolgreich geändert."}, status=status.HTTP_200_OK)
    
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        password = request.data.get('password')

        # Check if the provided password matches the user's actual password
        if not check_password(password, user.password):
            return Response({"detail": "Password is not correct."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete all authentication tokens related to the user
        Token.objects.filter(user=user).delete()

        # Finally, delete the user account
        user.delete()

        return Response({"detail": "Your account has been successfully deleted."}, status=status.HTTP_200_OK)
    
class AdminUserListView(generics.ListAPIView):
    serializer_class = AdminUserListSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be staff too

    def get_queryset(self):
        # Must be staff to see anything
        if not self.request.user.is_staff:
            return User.objects.none()

        qs = User.objects.all().order_by('email')
        search_query = self.request.query_params.get('search', None)
        if search_query:
            # Filter by partial match on email, first_name, or last_name
            qs = qs.filter(
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
        return qs