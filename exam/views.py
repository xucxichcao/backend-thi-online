from django.http import request
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import DeThi, DiemThi, PhongThi
from .serializers import getListPhongThi, themDeThi, thamGiaPhongThi


# Permission
class IsGiangVien(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.teacher


class isSinhVienAndReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.student
        return False


class isSinhVien(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.student

# Create your views here.


class giangVienDeThi(viewsets.ModelViewSet):
    permission_classes = (IsGiangVien, permissions.IsAuthenticated, )
    serializer_class = themDeThi

    def get_queryset(self):
        giangvien = self.request.user.gvinfo
        return DeThi.objects.filter(created_by=giangvien)

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user.gvinfo)


class viewPhongThi(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, isSinhVienAndReadOnly)
    serializer_class = thamGiaPhongThi

    def get_queryset(self):
        sinhvien = self.request.user.stinfo
        return DiemThi.objects.filter(sinhVien=sinhvien)


class viewListPhongThi(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, isSinhVienAndReadOnly)
    serializer_class = getListPhongThi

    def get_queryset(self):
        sinhvien = self.request.user.stinfo
        return PhongThi.objects.filter(diemthi__sinhVien=sinhvien)
