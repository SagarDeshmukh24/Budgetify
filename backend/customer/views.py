from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password

from .models import Customer
from .serializer import CustomerSerializer

# Customer API View
class CustomerAPI(APIView):
    
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            try:
                customer = Customer.objects.get(id=id)  # Corrected to .objects
            except Customer.DoesNotExist:
                return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

        customers = Customer.objects.all()  # Corrected to .objects
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def put(self, request, id):
        if id:
            try:
                customer = Customer.objects.get(id=id)  # Corrected to .objects
            except Customer.DoesNotExist:  # Corrected exception type
                return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response({"message": "Customer Deleted"}, status=status.HTTP_204_NO_CONTENT)

# Login API View
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
            customer = Customer.objects.get(email=email)
            
            serializer = CustomerSerializer(customer)
            # return Response(serializer.data)
            print(serializer.data)
            print(customer.password, customer.phone)
        
            # if password == serializer.data.password:
            if password == customer.password or check_password(password, customer.password):
                return Response(
                    {
                        "message": "Login successful",
                        "user": serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else: 
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Customer.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

# OTP Generation Function        
import random

def generate_otp():
    return str(random.randint(100000, 999999))

# Email OTP Function
from django.core.mail import send_mail
from django.conf import settings

def send_email_otp(email, otp):
    subject = "Budgetwala | Password Reset OTP"
    message = f"""
Hello,

Your OTP for password reset is: {otp}

This OTP is valid for 5 minutes.
If you did not request this, please ignore this email.

Regards,
Budgetwala Team
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )

# Telegram OTP Function
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_telegram_otp(chat_id, otp):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": (
            "🔐 Budgetwala Password Reset\n\n"
            f"Your OTP is: {otp}\n"
            "Valid for 5 minutes.\n\n"
            "If you didn’t request this, ignore."
        )
    }

    try:
        response = requests.post(url, json=payload, timeout=5)

        if response.status_code != 200:
            logger.error("Telegram error: %s", response.text)
            return False

        return True

    except requests.exceptions.RequestException as e:
        logger.exception("Telegram request failed")
        return False


# Forgot Password View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

@api_view(['POST'])
def forgot_password(request):
    email = request.data.get("email")
    telegram_chat_id = request.data.get("telegram_chat_id")

    if not email or not telegram_chat_id:
        return Response(
            {"error": "Email and Telegram Chat ID are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        customer = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        return Response(
            {"error": "Customer not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # 🔥 UPDATE / SAVE TELEGRAM CHAT ID
    customer.telegram_chat_id = telegram_chat_id
    customer.save()

    # Generate OTP
    otp = generate_otp()

    # Save OTP in session
    request.session["reset_otp"] = otp
    request.session["otp_expiry"] = (
        timezone.now() + timedelta(minutes=5)
    ).isoformat()
    request.session["reset_user"] = customer.id

    # Send OTP via Telegram
    sent = send_telegram_otp(telegram_chat_id, otp)

    if not sent:
        return Response(
            {"error": "Failed to send OTP via Telegram"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(
        {"message": "OTP sent successfully via Telegram"},
        status=status.HTTP_200_OK
    )



# Verify OTP View
from django.utils.dateparse import parse_datetime

@api_view(['POST'])
def verify_otp(request):
    entered_otp = request.data.get("otp")
    saved_otp = request.session.get("reset_otp")
    expiry = request.session.get("otp_expiry")

    if not saved_otp or not expiry:
        return Response(
            {"error": "OTP expired"},
            status=status.HTTP_400_BAD_REQUEST
        )

    expiry = parse_datetime(expiry)

    if timezone.now() > expiry:
        return Response(
            {"error": "OTP expired"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if entered_otp == saved_otp:
        return Response(
            {"message": "OTP verified"},
            status=status.HTTP_200_OK
        )

    return Response(
        {"error": "Invalid OTP"},
        status=status.HTTP_400_BAD_REQUEST
    )


# Reset Password View
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def reset_password(request):
    password = request.data.get("password")
    customer_id = request.session.get("reset_user")

    if not customer_id:
        return Response(
            {"error": "Session expired"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    customer.password = make_password(password)
    customer.save()

    request.session.flush()

    return Response(
        {"message": "Password reset successful"},
        status=status.HTTP_200_OK
    )
