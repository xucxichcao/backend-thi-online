from rest_framework import serializers
import csv
import io
from .models import DeThi


class themDeThi(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('soLuongCauHoi', 'file')
