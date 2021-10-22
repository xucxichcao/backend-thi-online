from django.db import models
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.db.models import constraints
from django.db.models.deletion import CASCADE
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

User = settings.AUTH_USER_MODEL


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    school = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False)
    student = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def role(self):
        return "Sinh viên" if self.student == True else "Giảng viên" if self.teacher == True else "Trường"


class Truong(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="scinfo", primary_key=True)
    school_name = models.CharField(blank=True, max_length=200)
    phone = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return self.school_name


class SinhVien(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="stinfo", primary_key=True)
    full_name = models.CharField(blank=True, max_length=40)
    sex = models.CharField(max_length=1, blank=True)
    cid = models.CharField(max_length=12, blank=True)
    sid = models.CharField(max_length=40, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    school = models.ForeignKey(Truong, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)


class GiangVien(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="gvinfo", primary_key=True)
    full_name = models.CharField(blank=True, max_length=40)
    sex = models.CharField(max_length=1, blank=True)
    cid = models.CharField(max_length=12, blank=True)
    sid = models.CharField(max_length=40, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    school = models.ForeignKey(Truong, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)


class DeThi(models.Model):
    soLuongCauHoi = models.PositiveSmallIntegerField()


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
    phongThi = models.ForeignKey(PhongThi, on_delete=CASCADE)
    diem = models.DecimalField(decimal_places=2, max_digits=4)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sinhVien', 'phongThi'], name="unique Sv PhongThi")
        ]


class accountBulkCreate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to="bulkAccount/")
    type = models.CharField(max_length=1, choices=(
        ('T', 'Giảng viên'), ('S', 'Sinh viên')), blank=False, default='S')

    def __str__(self):
        return self.csv_file.name
