from rest_framework import serializers
from .models import DeThi, DiemThi, PhongThi, ChiTietDeThi


class gvThemDeThi(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('soLuongCauHoi', 'file')


class svGetKeyDeThi(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('key')


class svGetDeThi(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('id', 'soLuongCauHoi')


class svGetListPhongThi(serializers.ModelSerializer):
    class Meta:
        model = PhongThi
        fields = ('tenPhongThi', 'siSo', 'giangVien',
                  'thoiGianLamBai', 'thoiGianThi', 'namHoc', 'hocKi')


class svGetChiTietDeThi(serializers.ModelSerializer):
    class Meta:
        model = ChiTietDeThi
        fields = ('questionID', 'noiDung')


class gvGetChiTietDeThi(serializers.ModelSerializer):
    class Meta:
        model = ChiTietDeThi
        fields = ('questionID', 'noiDung', 'dapAn')


class gvTaoPhongThi(serializers.ModelSerializer):
    class Meta:
        model = PhongThi
        fields = ('tenPhongThi', 'siSo', 'giangVien', 'danhSach', 'deThi',
                  'thoiGianLamBai', 'thoiGianThi', 'namHoc', 'hocKi')
