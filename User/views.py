from .models import UserModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']
        is_staff = request.data.get('is_staff',False)
        amount = request.data.get('amount',0)

        if UserModel.objects.filter(email=email).exists():
            return Response({"message": "You are already Registered"}, status=status.HTTP_400_BAD_REQUEST)
        user = UserModel.objects.create(email=email)
        user.set_password(password)
        
        if amount>0:
            user.wallet_balance = amount
        
        if is_staff:
            user.is_staff=True
        else:
            user.is_staff=False

        user.is_superuser=False        
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
                    "message": "Login successfully",
                    "refresh": refresh,
                    "access": refresh.access_token
                })
            else:
                return Response({"message":"Enter correct Password. Forgot?"})
        else:
            return Response({"message": "This email is not registered yet"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def recharge_wallet(request):
    if request.method=='PUT':
        email = request.data.get('email',None)
        if email is not None:
            user = UserModel.objects.get(email=email)
            amount = request.data.get('amount',0)
            if amount>0:
                balance = user.wallet_balance + request.data['amount']
            else:
                return Response({"message" : "Enter valid amount details"}, status=status.HTTP_400_BAD_REQUEST)
            user.wallet_balance = balance
            user.save()
            return Response({"message" : "Wallet Recharge Successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message" : "Email not found, Register First"}, status=status.HTTP_404_NOT_FOUND)