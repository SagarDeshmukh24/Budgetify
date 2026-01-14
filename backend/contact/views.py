import json
from django.http import JsonResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response

from .models import ContactMessage
from .serializer import ContactMessageSerializer


@method_decorator(csrf_exempt, name='dispatch')
class ContactAPI(APIView):

    # ✅ GET → for testing / admin / future use
    def get(self, request):
        messages = ContactMessage.objects.all()  # Corrected to .objects
        serializer = ContactMessageSerializer(messages, many=True)
        return Response(serializer.data)
       
    # ✅ POST → save contact message
    def post(self, request):
        try:
            data = json.loads(request.body)
            serializer = ContactMessageSerializer(data=request.data)
            name = data.get("name")
            email = data.get("email")
            message = data.get("message")

            if not name or not email or not message:
                return JsonResponse(
                    {"error": "All fields are required"},
                    status=400
                )
            elif serializer.is_valid():
                serializer.save()
                return JsonResponse(
                    {"success": True, "message": "Contact message saved"},
                    status=201
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"},
                status=400
            )
