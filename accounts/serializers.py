from django.db import models
from django.db.models import fields
from rest_framework import serializers

from accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'date_of_birth',
                  'cid', 'sid', 'phone', 'school_name']
