from .models import UserModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


@api_view(['POST'])
def signup(request):
    ''' 
        DESC : This method is used to sign up user
        Request Body : {"username" : "" , "password" : ""}
        Optional Field To create Staff user, used for adding Packs : {"is_staff" : "Yes"} 
        Returns : Token and Refresh Token with successful message
    '''
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        is_staff = request.data.get('is_staff',False)
        amount = request.data.get('amount',0)

        if UserModel.objects.filter(username=username).exists():
            return Response({"message": "You are already Registered"}, status=status.HTTP_400_BAD_REQUEST)
        user = UserModel.objects.create(username=username)
        user.set_password(password)
        
        if amount>0:
            user.wallet_balance = amount
        
        if is_staff == "Yes":
            user.is_staff=True
        else:
            user.is_staff=False

        user.is_superuser=False        
        user.save()
        refresh = RefreshToken.for_user(user)

        return Response({"message": "Account created successfully", "Token" : str(refresh.access_token) ,"Refresh_Token" : str(refresh)}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    ''' 
        DESC : This method is used to login
        Request Body : {"username" : "" , "password" : ""}
        Returns : Token and Refresh Token with successful message
    '''
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']

        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            haspassword = user.password
            if check_password(password, haspassword):
                user = authenticate(username=username, password=password)
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                })
            else:
                return Response({"message":"Enter correct Password. Forgot?"})
        else:
            return Response({"message": "This username is not registered yet"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def recharge_wallet(request):
    ''' 
        DESC : This method is used to add money to the User wallet
        Request Body : { "amount" : "200" }
        Returns : Successful Message with Wallet balance
    '''
    if request.method=='PUT':
        username = request.user

        user = UserModel.objects.get(username=username)
        amount = request.data.get('amount',0)
        if amount>0:
            balance = user.wallet_balance + request.data['amount']
        else:
            return Response({"message" : "Enter valid amount details"}, status=status.HTTP_400_BAD_REQUEST)
        user.wallet_balance = balance
        user.save()
        return Response({"message" : "Wallet Recharge Successful", "Wallet_Balance" : f"Rs.{balance}"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_balance(request):
    ''' 
        DESC : This method is used to add money to the User wallet
        No Request Body or Query Parameters Required
        Returns : Wallet Balance
    '''
    username = request.user
    user = UserModel.objects.get(username = username)
    return Response({"success":True, "Wallet_Balance":f"Rs.{user.wallet_balance}"})