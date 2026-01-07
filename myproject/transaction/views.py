from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Transaction
from .serializer import TransactionSerializer

# Create your views here.

class TransactionAPI(APIView):
    
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            try:
                transaction = Transaction.objects.get(id=id)  # Corrected to .objects
            except Transaction.DoesNotExist:
                return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)

        transactions = Transaction.objects.all()  # Corrected to .objects
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def put(self, request, id):
        if id:
            try:
                transaction = Transaction.objects.get(id=id)  # Corrected to .objects
            except Transaction.DoesNotExist:  # Corrected exception type
                return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = TransactionSerializer(transaction, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            transaction = Transaction.objects.get(id=id)
        except Transaction.DoesNotExist:
            return Response({'error': "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        transaction.delete()
        return Response({"message": "Customer Deleted"}, status=status.HTTP_204_NO_CONTENT)
