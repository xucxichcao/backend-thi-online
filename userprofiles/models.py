from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL


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
