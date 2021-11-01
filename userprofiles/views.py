from django.shortcuts import render
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from .models import Truong, SinhVien, GiangVien
from .serializers import TruongSerializer, SinhVienSerializer, GiangVienSerializer


# Permissions
class isGiangVienAndOwned(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.teacher

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class isSinhVienAndOwned(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.student

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class isTruongAndOwned(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.school

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

# Create your views here.


class viewProfile(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.UpdateModelMixin):
    def get_permissions(self):
        if self.request.user.school:
            self.permission_classes = (
                permissions.IsAuthenticated, isTruongAndOwned)
        elif self.request.user.teacher:
            self.permission_classes = (
                permissions.IsAuthenticated, isGiangVienAndOwned)
        elif self.request.user.student:
            self.permission_classes = (
                permissions.IsAuthenticated, isSinhVienAndOwned)
        return super(viewProfile, self).get_permissions()

    def get_serializer_class(self):
        if self.request.user.school:
            return TruongSerializer
        elif self.request.user.teacher:
            return GiangVienSerializer
        elif self.request.user.student:
            return SinhVienSerializer

    def get_queryset(self):
        user = self.request.user
        if user.school:
            return Truong.objects.filter(user=user)
        elif user.teacher:
            return GiangVien.objects.filter(user=user)
        elif user.student:
            return SinhVien.objects.filter(user=user)

    def put(self, request, *args, **kwargs):
        user = self.request.user
        if 'phone' in self.request.data:
            if user.school:
                instance = Truong.objects.get(user=user)
            elif user.teacher:
                instance = GiangVien.objects.get(user=user)
            elif user.student:
                instance = SinhVien.objects.get(user=user)
            serializer = self.get_serializer(
                instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({"message": "Không có thông tin cập nhật"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()
