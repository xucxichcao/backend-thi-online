from rest_framework import serializers
from .models import DeThi


class themDeThi(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('soLuongCauHoi', 'file')
