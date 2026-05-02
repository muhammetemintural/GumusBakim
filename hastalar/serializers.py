from rest_framework import serializers
from .models import HastaIlac, Hasta
from ziyaretler.models import Ziyaret # Ziyaret modelini ekledik

class HastaIlacSerializer(serializers.ModelSerializer):
    class Meta:
        model = HastaIlac
        fields = '__all__'

# Sadece Serializer burada kalmalı
class ZiyaretSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ziyaret
        fields = '__all__'