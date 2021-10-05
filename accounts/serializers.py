from rest_framework import serializers

from accounts.models import CustomUser, accountBulkCreate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'date_of_birth',
                  'cid', 'sid', 'phone', 'school_name']


class AccountBulkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountBulkCreate
        fields = ('user', 'csv_file')
