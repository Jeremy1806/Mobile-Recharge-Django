from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from User.models import UserModel
from .models import RechargePack
from recharge.serializer import PackCreateSerializer

@api_view(['POST'])
def add_recharge_pack(request):
    if request.method == 'POST':
        print(request.data)
        username = request.data.get('username',None)
        price = int(request.data.get('pack_price'))
        if username is not None :
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
                    return Response({"message":"Pack Added Successfully"},status=status.HTTP_200_OK)
                except:
                    return Response({"message" : "Server Error !! Try Again"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"message" : "Access Denied !! You have no permission"}, status=status.HTTP_403_FORBIDDEN)

        else:
            return {"message" : "Invalid Request!! Check username or price"}