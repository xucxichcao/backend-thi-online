from django.db import models
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import GiangVien, SinhVien, Truong
from accounts.models import CustomUser


class SinhVienSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source="user.avatar")
    email = serializers.EmailField(source="user.email")
    school = serializers.SlugRelatedField(
        slug_field="school_name", read_only=True)

    class Meta:
        model = SinhVien
        fields = ('email', 'avatar', 'full_name', 'sex', 'cid', 'sid',
                  'phone', 'school', 'date_of_birth')
        read_only_fields = ('email', 'full_name', 'sex', 'cid',
                            'sid', 'school', 'date_of_birth')


class GiangVienSerializer(serializers.ModelSerializer):
    school = serializers.SlugRelatedField(
        slug_field="school_name", read_only=True)
    avatar = serializers.ImageField(source="user.avatar")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = GiangVien
        fields = ('email', 'avatar', 'full_name', 'sex', 'cid', 'sid',
                  'phone', 'school', 'date_of_birth')
        read_only_fields = ('email', 'full_name', 'sex', 'cid',
                            'sid', 'school', 'date_of_birth')


class TruongSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source="user.avatar")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Truong
        fields = ('email', 'avatar', 'school_name', 'phone')
        read_only_fields = ('email',)


class TruongCreateProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Truong
        fields = ('user', 'school_name', 'phone')
