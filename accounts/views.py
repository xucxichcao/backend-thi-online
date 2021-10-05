from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import accountBulkCreate
from .serializers import AccountBulkCreateSerializer

# Permission


class IsSchoolAccount(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.school


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

# Create your views here.


class AccountBulkCreateViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSchoolAccount, )
    serializer_class = AccountBulkCreateSerializer

    def get_queryset(self):
        user = self.request.user
        return accountBulkCreate.objects.filter(user=user)
