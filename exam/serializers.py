from rest_framework import serializers
from .models import DeThi, DiemThi, PhongThi, ChiTietDeThi


class svGetListPhongThi(serializers.ModelSerializer):
    diem = serializers.SerializerMethodField()

    def get_diem(self, obj):
        user = self.context.get('request').user
        pt = obj
        return DiemThi.objects.get(sinhVien__user=user, phongThi=pt).diem

    class Meta:
        model = PhongThi
        fields = ('id', 'tenPhongThi', 'siSo', 'giangVien',
                  'thoiGianLamBai', 'thoiGianThi', 'namHoc', 'hocKi', 'diem')


class svGetKeyDeThi(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('key',)


class svGetDeThi(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('id', 'soLuongCauHoi')


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


class gvThemDeThi(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('soLuongCauHoi', 'file', 'createdBy')


class gvGetChiTietDeThi(serializers.ModelSerializer):
    class Meta:
        model = ChiTietDeThi
        fields = ('questionID', 'noiDung', 'dapAn')


class gvPhongThi(serializers.ModelSerializer):
    class Meta:
        model = PhongThi
        fields = ('id', 'tenPhongThi', 'siSo', 'giangVien', 'danhSach', 'deThi',
                  'thoiGianLamBai', 'thoiGianThi', 'namHoc', 'hocKi')
