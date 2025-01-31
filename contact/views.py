# contact/views.py

import requests
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Contact
from .serializers import ContactSerializer
from django.conf import settings

class ContactFormView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            recaptcha_token = serializer.validated_data.pop('recaptcha_token')
            recaptcha_secret_key = settings.RECAPTCHA_SECRET_KEY

            # Verify reCAPTCHA
            recaptcha_response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data={
                    'secret': recaptcha_secret_key,
                    'response': recaptcha_token
                }
            )
            result = recaptcha_response.json()

            if not result.get('success'):
                return Response(
                    {"detail": "reCAPTCHA verification failed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Optionally, check the score or other parameters if using reCAPTCHA v3

            # Save the contact message
            serializer.save()
            return Response({"detail": "Message received."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminMessagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        
        messages = Contact.objects.all().order_by('-created_at')
        serializer = ContactSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
