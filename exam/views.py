import datetime
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import DeThi, DiemThi, PhongThi, ChiTietDeThi
from .serializers import gvPhongThi, svGetDiem, svGetIDThamGia, svGetKeyDeThi, gvGetChiTietDeThi, svGetChiTietDeThi, svGetListPhongThi, svGetDeThi, gvThemDeThi, svLamBaiThi


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

    def has_object_permission(self, request, view, obj):
        return request.user.student


class isGiangVienAndOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.teacher

    def has_object_permission(self, request, view, obj):
        return obj.deThi.createdBy.user == request.user


# Create your views here.
class svViewListPhongThi(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, isSinhVienAndReadOnly)
    serializer_class = svGetListPhongThi

    def get_queryset(self):
        user = self.request.user
        return PhongThi.objects.filter(diemthi__sinhVien__user=user)


class svViewGetDeThi(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, isSinhVienAndReadOnly, )
    serializer_class = svGetDeThi

    def get_queryset(self):
        if "idPhongThi" in self.request.data:
            return DeThi.objects.filter(phongthi__id=self.request.data['idPhongThi'], phongthi__diemthi__sinhVien__user=self.request.user)
        else:
            return DeThi.objects.none()


class svViewGetIDThamGia(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, isSinhVienAndReadOnly, )
    serializer_class = svGetIDThamGia

    def get_queryset(self):
        if "idPhongThi" in self.request.data:
            return DiemThi.objects.filter(phongThi__id=self.request.data['idPhongThi'], sinhVien__user=self.request.user)
        else:
            return DiemThi.objects.none()


class svViewGetKeyDeThi(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, isSinhVienAndReadOnly, )
    serializer_class = svGetKeyDeThi

    def get_queryset(self):
        if "idPhongThi" in self.request.data:
            return DeThi.objects.filter(phongthi__thoiGianThi__lte=datetime.datetime.now(), phongthi__id=self.request.data['idPhongThi'])
        else:
            return DeThi.objects.none()


class svCTDT(viewsets.ModelViewSet):
    serializer_class = svGetChiTietDeThi
    permission_classes = (isSinhVienAndReadOnly, )

    def get_queryset(self):
        if "key" in self.request.data:
            return ChiTietDeThi.objects.filter(deThi__key=self.request.data['key'])
        else:
            return ChiTietDeThi.objects.none()


class svViewDiem(viewsets.ModelViewSet):
    serializer_class = svGetDiem
    permission_classes = (isSinhVienAndReadOnly, )

    def get_queryset(self):
        if "phongThiID" in self.request.data:
            user = self.request.user
            return DiemThi.objects.filter(sinhVien__user=user, phongThi__id=self.request.data['phongThiID'])
        else:
            return DiemThi.objects.none()


class svViewLamBai(viewsets.ModelViewSet):
    serializer_class = svLamBaiThi
    permission_classes = (isSinhVien,)

    def list(self, request, *args, **kwargs):
        response = {'message': 'Only PUT method is allowed'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        response = {'message': 'Only PUT method is allowed'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Only PUT method is allowed'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        if "idPhongThi" in self.request.data:
            dt = DiemThi.objects.get(
                phongThi__id=self.request.data['idPhongThi'], sinhVien__user=self.request.user)
            pt = dt.phongThi
            time = pt.thoiGianThi
            timeplus = pt.thoiGianLamBai
            if datetime.datetime.now() > time and datetime.datetime.now() < (time + datetime.timedelta(minutes=timeplus)):
                return super().update(request, *args, **kwargs)
        return Response({'message': 'Không trong thời gian làm bài'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'Only PUT method is allowed'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        response = {'message': 'Only PUT method is allowed'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class gvViewPhongThi(viewsets.ModelViewSet):
    permission_classes = (isGiangVienAndOwner, permissions.IsAuthenticated, )
    serializer_class = gvPhongThi

    def get_queryset(self):
        return PhongThi.objects.filter(giangVien__user=self.request.user)


class gvThemDeThi(viewsets.ModelViewSet):
    permission_classes = (isGiangVienAndOwner, permissions.IsAuthenticated, )
    serializer_class = gvThemDeThi

    def get_queryset(self):
        user = self.request.user
        return DeThi.objects.filter(createdBy__user=user)

    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(createdBy=req.user.gvinfo)


class gvCTDT(viewsets.ModelViewSet):
    serializer_class = gvGetChiTietDeThi
    permission_classes = (isGiangVienAndOwner, )

    def get_queryset(self):
        user = self.request.user
        return ChiTietDeThi.objects.filter(deThi__createdBy__user=user)
