from django.db import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import GiangVien, SinhVien, Truong


class SinhVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinhVien
        fields = ['full_name', 'sex', 'cid', 'sid',
                  'phone', 'school', 'date_of_birth']


class GiangVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiangVien
        fields = ['full_name', 'sex', 'cid', 'sid',
                  'phone', 'school', 'date_of_birth']


class TruongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truong
        fields = ['school_name', 'phone']
