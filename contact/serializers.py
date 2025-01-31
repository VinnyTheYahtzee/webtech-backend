# contact/serializers.py

from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    recaptcha_token = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'message', 'created_at', 'recaptcha_token']
        read_only_fields = ['id', 'created_at']
