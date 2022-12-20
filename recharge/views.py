from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from User.models import UserModel
from .models import RechargePack, MakeRecharge
from recharge.serializer import PackCreateSerializer
from django.core.serializers import serialize
import json
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_recharge_pack(request):
    if request.method == 'POST':
        username = request.user
        price = int(request.data.get('pack_price'))
        if not RechargePack.objects.filter(pack_price = price).exists():
            try:
                user = UserModel.objects.get(username=username)
            except:
                return Response({"message" : "username is not Registered. Register as staff to add packs."}, status=status.HTTP_400_BAD_REQUEST)

            if user.is_staff:                
                temp = PackCreateSerializer(data=request.data)
                temp.is_valid(raise_exception=True)
                print(request.data)
                try:
                    temp.save()
                    return Response({"message":"Pack Added Successfully"},status=status.HTTP_201_CREATED)
                except:
                    return Response({"message" : "Server Error !! Try Again"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"message" : "Access Denied !! You have no permission"}, status=status.HTTP_403_FORBIDDEN)

        else:
            return Response({"message" : "Invalid Request!! Check username or price"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_packs(request):
    operator = request.data.get('pack_operator')
    query_set = RechargePack.objects.all()
    query_set = query_set.filter(pack_operator = operator)
    ser_data = serialize("json" , queryset=query_set)
    response = json.loads(ser_data)
    response1 = []
    for data in response:
        response1.append(data["fields"])
    return Response({"success":True , "data" : response1},  status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_recharge(request):
    if request.method == 'POST':
        username = request.user
        price = int(request.data.get("price"))
        number = request.data.get("phone_number")
        operator = request.data.get("operator")

        user = UserModel.objects.get(username = username)
        balance = user.wallet_balance
        try:
            recharge_pack = RechargePack.objects.filter(pack_price=price,pack_operator = operator).first()
        except:
            return Response({"message":"Pack Not Found !! Enter valid details"})
        if balance<price:
            return Response({"message":"Insufficient Balance in Wallet. Try Another payment method or recharge wallet"}, status=status.HTTP_400_BAD_REQUEST)
        
        rechargeIns = MakeRecharge.objects.create(user = user, recharge_pack = recharge_pack,phone_number = number,operator=operator,price=price,status = 'Completed')
        rechargeIns.save()
        user.wallet_balance = balance-price
        user.save()
        return Response({"message":"Transaction Succesful","Wallet_Balance" : f"Rs.{balance-price}" },status=status.HTTP_201_CREATED)