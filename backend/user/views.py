from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
import requests
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import User
from .serializer import UserSerializer

# Create your views here.
BOT_TOKEN = "7657831643:AAEUHfryt9fUzHsXShtiOtn7U3D9_Wj1ysg"
CHAT_ID = "8029148711"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

@csrf_exempt
def forgot_password(request):
    if request.method == "POST":

        data = json.loads(request.body)
        email = data.get("email")

        # 1️⃣ email exist hai ya nahi
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "Email not registered"},
                status=400
            )

        # 2️⃣ OTP generate
        otp = random.randint(100000, 999999)

        # 3️⃣ OTP DB me save
        user.reset_otp = otp
        user.save()

        # 4️⃣ Telegram pe OTP bhejo
        send_telegram_message(
            f"Your password reset OTP is: {otp}"
        )

        # 5️⃣ response
        return JsonResponse(
            {"message": "OTP sent to Telegram"}
        )
    
@csrf_exempt
def verify_otp(request):
    if request.method == "POST":

        data = json.loads(request.body)
        email = data.get("email")
        otp = data.get("otp")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "Invalid email"},
                status=400
            )

        if str(user.reset_otp) != str(otp):
            return JsonResponse(
                {"error": "Invalid OTP"},
                status=400,
            )

        return JsonResponse(
            {"message": "OTP verified"}
        )

@csrf_exempt
def reset_password(request):
    if request.method == "POST":

        data = json.loads(request.body)
        email = data.get("email")
        new_password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "Invalid email"},
                status=400
            )

        # password update
        user.password = new_password
        user.reset_otp = None
        user.save()

        return JsonResponse(
            {"message": "Password reset successful"}
        )

class UserAPI(APIView):
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            try:
                customer = User.objects.get(id=id)  # Corrected to .objects
            except User.DoesNotExist:
                return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(customer)
            return Response(serializer.data)

        users = User.objects.all()  # Corrected to .objects
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def put(self, request, id):
        if id:
            try:
                user = User.objects.get(id=id)  # Corrected to .objects
            except User.DoesNotExist:  # Corrected exception type
                return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"message": "Customer Deleted"}, status=status.HTTP_204_NO_CONTENT)


class LoginAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            
            serializer = UserSerializer(user)
            # return Response(serializer.data)
            print(serializer.data)
            print(user.password, user.phone)
        
            # if password == serializer.data.password:
            if password == user.password or check_password(password, user.password):
                return Response(
                    {
                        "message": "Login successful",
                        "user": serializer.data
                        # "user": {
                        #     "id": serializer.data.id,
                        #     "name": serializer.data.name,
                        #     "email": serializer.data.email,
                        #     "phone": serializer.data.phone,
                        #     "type": serializer.data.type,
                        #     "created_at": serializer.data.created_at
                        # }
                    },
                    status=status.HTTP_200_OK
                )
            else: 
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )