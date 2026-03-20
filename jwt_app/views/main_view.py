from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..models import Product
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import UserSerializer, ProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_view(request):
    if request.method == 'GET':
        products = Product.objects.filter(user=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Product created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)