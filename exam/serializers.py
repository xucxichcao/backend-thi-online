from django.db.models import fields
from rest_framework import serializers, permissions
from .models import DeThi, DiemThi, PhongThi


class themDeThi(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('soLuongCauHoi', 'file')


class getKeyDeThi(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('key')


class thamGiaPhongThi(serializers.ModelSerializer):
    class Meta:
        model = DiemThi
        fields = ('phongThi', 'sinhVien', 'diem')


class getListPhongThi(serializers.ModelSerializer):
    class Meta:
        model = PhongThi
        fields = ('tenPhongThi', 'siSo', 'giangVien',
                  'thoiGianLamBai', 'thoiGianThi', 'namHoc', 'hocKi')
