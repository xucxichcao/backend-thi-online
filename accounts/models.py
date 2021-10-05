from django.db import models
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.db.models.fields.files import FileField
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    full_name = models.CharField(blank=True, max_length=40)
    sex = models.CharField(max_length=1, blank=True)
    cid = models.CharField(max_length=12, blank=True)
    sid = models.CharField(max_length=40, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    school_name = models.CharField(blank=True, max_length=200)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.email

    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff


class accountBulkCreate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csv_file = FileField(upload_to="bulkAccount/")
    type = models.CharField(max_length=1, choices=(
        ('T', 'Giảng viên'), ('S', 'Sinh viên')), blank=False, default='S')

    def __str__(self):
        return self.csv_file.name
