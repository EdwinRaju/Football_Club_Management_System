# serializers.py
from rest_framework import serializers
from .models import CustomUser

class PlayerEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

from rest_framework import serializers
from .models import CustomUser

class CoachEmailSerializer(serializers.Serializer):
    coach_email = serializers.EmailField()
