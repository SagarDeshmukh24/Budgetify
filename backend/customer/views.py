from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
import requests
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import Customer
from .serializer import CustomerSerializer

# Create your views here.

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
        except Customer.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )