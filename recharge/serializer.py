from rest_framework import serializers
from recharge.models import RechargePack

class PackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RechargePack
        fields = '__all__'