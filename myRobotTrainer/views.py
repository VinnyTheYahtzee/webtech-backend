from django.http import JsonResponse
from django.conf import settings
from django.db import connection

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ok", "database": settings.DATABASES.get("default", "Not Configured")})
    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)}, status=500)