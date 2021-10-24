from django.db import models
from accounts.models import GiangVien, SinhVien
# Create your models here.


class DeThi(models.Model):
    soLuongCauHoi = models.PositiveSmallIntegerField()
    file = models.FileField(upload_to="deThi/")


class ChiTietDeThi(models.Model):
    deThi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    noiDung = models.TextField()
    dapAn = models.PositiveSmallIntegerField()


class PhongThi(models.Model):
    tenPhongThi = models.CharField(blank=True, max_length=200)
    siSo = models.PositiveSmallIntegerField()
    giangVien = models.ForeignKey(GiangVien, on_delete=models.CASCADE)
    danhSach = models.FileField(upload_to="danhSachPhongThi/")
    deThi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    thoiGianLamBai = models.PositiveSmallIntegerField()
    thoiGianThi = models.DateTimeField()
    namHoc = models.CharField(max_length=11)
    hocKi = models.PositiveIntegerField()


class DiemThi(models.Model):
    sinhVien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    phongThi = models.ForeignKey(PhongThi, on_delete=models.CASCADE)
    diem = models.DecimalField(decimal_places=2, max_digits=4)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sinhVien', 'phongThi'], name="unique Sv PhongThi")
        ]
