from rest_framework import serializers

from userprofiles.models import GiangVien
from .models import DeThi, DiemThi, PhongThi, ChiTietDeThi


class svGetListPhongThi(serializers.ModelSerializer):
    diem = serializers.SerializerMethodField()
    giangVien_name = serializers.ReadOnlyField(source='giangVien.full_name')

    def get_diem(self, obj):
        user = self.context.get('request').user
        pt = obj
        return DiemThi.objects.get(sinhVien__user=user, phongThi=pt).diem

    class Meta:
        model = PhongThi
        fields = ('id', 'tenPhongThi', 'siSo', 'giangVien',
                  'thoiGianLamBai', 'thoiGianThi', 'namHoc', 'hocKi', 'diem', 'giangVien_name')


class svGetKeyDeThi(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('key',)


class svGetDeThi(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('id', 'soLuongCauHoi', 'kieuThi')


class svGetDeThiTuLuan(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('id', 'kieuThi', 'file')


class svGetChiTietDeThi(serializers.ModelSerializer):
    class Meta:
        model = ChiTietDeThi
        fields = ('questionID', 'noiDung')


class svLamBaiThi(serializers.ModelSerializer):
    class Meta:
        model = DiemThi
        fields = ('phongThi', 'baiLam')


class svLamBaiThiTuLuan(serializers.ModelSerializer):
    class Meta:
        model = DiemThi
        fields = ('phongThi', 'baiLamTuLuan')


class svGetDiem(serializers.ModelSerializer):
    class Meta:
        model = DiemThi
        fields = ('phongThi', 'diem')


class gvThemDeThiSer(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('soLuongCauHoi', 'file', 'createdBy', 'kieuThi')
        read_only_fields = ('createdBy',)


class gvGetDeTuLuan(serializers.ModelSerializer):
    class Meta:
        model = DeThi
        fields = ('file',)
        read_only_fields = ('file',)


class gvGetChiTietDeThi(serializers.ModelSerializer):
    class Meta:
        model = ChiTietDeThi
        fields = ('questionID', 'noiDung', 'dapAn')


class gvPhongThi(serializers.ModelSerializer):
    giangVien_name = serializers.ReadOnlyField(source='giangVien.full_name')

    class Meta:
        model = PhongThi
        fields = ('id', 'tenPhongThi', 'siSo', 'giangVien', 'danhSach', 'deThi',
                  'thoiGianLamBai', 'thoiGianThi', 'namHoc', 'hocKi', 'giangVien_name')
        read_only_fields = ('giangVien',)


class DiemAll(serializers.ModelSerializer):
    sinhVien_name = serializers.ReadOnlyField(source="sinhVien.full_name")

    class Meta:
        model = DiemThi
        fields = ('sinhVien', 'diem', 'sinhVien_name')


class schoolPhongThi(serializers.ModelSerializer):
    giangVien_name = serializers.ReadOnlyField(source='giangVien.full_name')

    class Meta:
        model = PhongThi
        fields = ('id', 'tenPhongThi', 'siSo', 'giangVien', 'danhSach', 'deThi',
                  'thoiGianLamBai', 'thoiGianThi', 'namHoc', 'hocKi', 'giangVien_name')
