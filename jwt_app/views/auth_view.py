from rest_framework import response, status
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from ..serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        return print(username, email, password)