from django.http import JsonResponse

def health_check(request):
    """
    Simple health check endpoint for Render.
    Returns HTTP 200 with {"status": "ok"}.
    Does NOT expose any secrets, keys, or database info.
    """
    return JsonResponse({"status": "ok"})
