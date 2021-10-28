import time
import hashlib
from django.db import models
from userprofiles.models import GiangVien, SinhVien
# Create your models here.


def _createHash():
    """This function generate 10 character long hash"""
    hash = hashlib.sha1()
    hash.update(str(time.time()))
    return hash.hexdigest()[:-8]


class DeThi(models.Model):
    soLuongCauHoi = models.PositiveSmallIntegerField()
    file = models.FileField(upload_to="deThi/")
    key = models.CharField(max_length=8, default=_createHash, unique=True)
    createdBy = models.ForeignKey(
        GiangVien, on_delete=models.CASCADE)


class ChiTietDeThi(models.Model):
    deThi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    questionID = models.PositiveSmallIntegerField()
    noiDung = models.TextField()
    dapAn = models.PositiveSmallIntegerField()


class PhongThi(models.Model):
    tenPhongThi = models.CharField(blank=True, max_length=200)
    siSo = models.PositiveSmallIntegerField()
    giangVien = models.ForeignKey(GiangVien, on_delete=models.CASCADE)
    danhSach = models.FileField(upload_to="danhSachPhongThi/")
    deThi = models.OneToOneField(
        DeThi, related_name='phongthi', on_delete=models.CASCADE)
    thoiGianLamBai = models.PositiveSmallIntegerField()
    thoiGianThi = models.DateTimeField()
    namHoc = models.CharField(max_length=11)
    hocKi = models.PositiveIntegerField()


class DiemThi(models.Model):
    sinhVien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    phongThi = models.ForeignKey(PhongThi, on_delete=models.CASCADE)
    baiLam = models.TextField(blank=True)
    diem = models.DecimalField(
        decimal_places=2, max_digits=4, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sinhVien', 'phongThi'], name="unique Sv PhongThi")
        ]
