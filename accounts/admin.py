from django.contrib import admin
from .models import CustomUser, SinhVien, GiangVien, Truong

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(SinhVien)
admin.site.register(GiangVien)
admin.site.register(Truong)
