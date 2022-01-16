import time
import hashlib
from django.db import models
from userprofiles.models import GiangVien, SinhVien
# Create your models here.


def _createHash():
    """This function generate 8 character long hash"""
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode('utf-8'))
    return hash.hexdigest()[:8]


KIEUTHI_CHOICES = ((False, "Tự luận"), (True, "Trắc nghiệm"),)


class DeThi(models.Model):
    kieuThi = models.BooleanField(choices=KIEUTHI_CHOICES, default=True)
    soLuongCauHoi = models.PositiveSmallIntegerField()
    file = models.FileField(upload_to="deThi/")
    key = models.CharField(max_length=8, default=_createHash, unique=True)
    createdBy = models.ForeignKey(
        GiangVien, on_delete=models.CASCADE)

    # def __str__(self):
    #     return str(self.phongthi)


class ChiTietDeThi(models.Model):
    deThi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    questionID = models.PositiveSmallIntegerField()
    noiDung = models.TextField()
    dapAn = models.PositiveSmallIntegerField()

    # def __str__(self):
    # return str(self.deThi) + " - câu " + str(self.questionID+1)


class PhongThi(models.Model):
    tenPhongThi = models.CharField(blank=True, max_length=200)
    siSo = models.PositiveSmallIntegerField()
    giangVien = models.ForeignKey(GiangVien, on_delete=models.CASCADE)
    danhSach = models.FileField(upload_to="danhSachPhongThi/")
    deThi = models.OneToOneField(
        DeThi, related_name='phongthi', on_delete=models.CASCADE, null=True, blank=True)
    thoiGianLamBai = models.PositiveSmallIntegerField()
    thoiGianThi = models.DateTimeField()
    namHoc = models.CharField(max_length=11)
    hocKi = models.PositiveIntegerField()
    # def __str__(self):
    #     return str(self.tenPhongThi) + " - " + str(self.giangVien)


class DiemThi(models.Model):
    sinhVien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    phongThi = models.ForeignKey(PhongThi, on_delete=models.CASCADE)
    baiLam = models.TextField(blank=True)
    diem = models.DecimalField(
        decimal_places=2, max_digits=4, null=True, blank=True)
    baiLamTuLuan = models.FileField(upload_to="baiLamTuLuan/", blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sinhVien', 'phongThi'], name="unique Sv PhongThi")
        ]

class DiemTuLuan(models.Model):
    phongThi = models.ForeignKey(PhongThi, on_delete=models.CASCADE)
    fileDiem = models.FileField(upload_to="diemTuLuan/")