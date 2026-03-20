from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not email or not password:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        if user is not None:
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Failed to create user.'}, status=status.HTTP_400_BAD_REQUEST)

def get_token_for_user(user):
    token = RefreshToken.for_user(user)
    return {
        'refresh': str(token),
        'access': str(token.access_token),
    }
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    errors = {}
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username:
            errors['error'] = 'Username and password are required.'
            
        if not password:
            errors['error'] = 'Username and password are required.'
            
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = get_token_for_user(user)
        return Response({"msg": "Login successful.", "token": token, "user": user}, status=status.HTTP_200_OK)