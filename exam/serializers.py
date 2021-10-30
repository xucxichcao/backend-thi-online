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
        fields = ('id', 'tenPhongThi', 'siSo', 'giangVien',
                  'thoiGianLamBai', 'thoiGianThi', 'namHoc', 'hocKi')


class svGetChiTietDeThi(serializers.ModelSerializer):
    class Meta:
        model = ChiTietDeThi
        fields = ('questionID', 'noiDung')


class svLamBaiThi(serializers.ModelSerializer):
    class Meta:
        model = DiemThi
        fields = ('phongThi', 'baiLam')


class svGetDiem(serializers.ModelSerializer):
    class Meta:
        model = DiemThi
        fields = ('phongThi', 'diem')


class gvGetChiTietDeThi(serializers.ModelSerializer):
    class Meta:
        model = ChiTietDeThi
        fields = ('questionID', 'noiDung', 'dapAn')


class gvPhongThi(serializers.ModelSerializer):
    class Meta:
        model = PhongThi
        fields = ('tenPhongThi', 'siSo', 'giangVien', 'danhSach', 'deThi',
                  'thoiGianLamBai', 'thoiGianThi', 'namHoc', 'hocKi')
