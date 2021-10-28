from django.http import request
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import DeThi, DiemThi, PhongThi, ChiTietDeThi
from .serializers import gvGetChiTietDeThi, svGetChiTietDeThi, getListPhongThi, themDeThi, thamGiaPhongThi


# Permission
class isGiangVien(permissions.BasePermission):
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


class isGiangVienAndOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.teacher

    def has_object_permission(self, request, view, obj):
        return obj.deThi.createdBy == request.user.gvinfo

# Create your views here.


class giangVienDeThi(viewsets.ModelViewSet):
    permission_classes = (isGiangVien, permissions.IsAuthenticated, )
    serializer_class = themDeThi

    def get_queryset(self):
        giangvien = self.request.user.gvinfo
        return DeThi.objects.filter(createdBy=giangvien)

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


class svCTDT(viewsets.ModelViewSet):
    serializer_class = svGetChiTietDeThi
    permission_classes = (isSinhVienAndReadOnly, )

    def get_queryset(self):
        if "key" in self.request.data:
            return ChiTietDeThi.objects.filter(deThi__key=self.request.data['key'])
        else:
            return ChiTietDeThi.objects.none()


class gvCTDT(viewsets.ModelViewSet):
    serializer_class = gvGetChiTietDeThi
    permission_classes = (isGiangVienAndOwner, )

    def get_queryset(self):
        giangvien = self.request.user.gvinfo
        return ChiTietDeThi.objects.filter(deThi__createdBy=giangvien)
