from .models import UserModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']

        if UserModel.objects.filter(email=email).exists():
            return Response({"messege": "You are already Registered"}, status=status.HTTP_400_BAD_REQUEST)
        user = UserModel.objects.create(email=email)
        user.set_password(password)
        user.save()
        return Response({"message": "Account created successfully"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']

        if UserModel.objects.filter(email=email).exists():
            user = UserModel.objects.get(email=email)
            haspassword = user.password
            if check_password(password, haspassword):
                user = authenticate(email=email, password=password)
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "message": "Login successfully"
                })
        else:
            return Response({"message": "Account not found"}, status=status.HTTP_400_BAD_REQUEST)
