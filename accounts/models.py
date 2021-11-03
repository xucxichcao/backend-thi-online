from django.db import models
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

User = settings.AUTH_USER_MODEL


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(
        upload_to="avatar/", default='avatar/default.png')
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    school = models.BooleanField(default=True)
    teacher = models.BooleanField(default=False)
    student = models.BooleanField(default=False)

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


class accountBulkCreate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to="bulkAccount/")
    type = models.CharField(max_length=1, choices=(
        ('T', 'Giảng viên'), ('S', 'Sinh viên')), blank=False, default='S')

    def __str__(self):
        return self.csv_file.name
