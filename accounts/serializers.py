from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import csv
import io
from datetime import datetime
from allauth.account.models import EmailAddress
from accounts.models import CustomUser, accountBulkCreate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'date_of_birth',
                  'cid', 'sid', 'phone', 'school_name']


class AccountBulkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountBulkCreate
        fields = ('user', 'csv_file', 'type')

    def create(self, validated_data):
        accType = validated_data.get('type')
        if(accType == 'S'):
            csv_file = validated_data.get('csv_file')
            decoded_file = csv_file.read().decode('utf-8')
            io_strings = io.StringIO(decoded_file)
            csvf = csv.reader(io_strings)
            for row in csvf:
                try:
                    user = User(sid=row[0], email=row[1], full_name=row[2],
                                sex=row[3], cid=row[4], phone=row[5], date_of_birth=datetime.strptime(row[6], '%d-%m-%Y'))
                    user.password = make_password("freepassword")
                    user.save()
                    newEmail = EmailAddress(
                        user=user, email=row[1], verified=True)
                    newEmail.save()
                except:
                    continue
        elif(accType == 'T'):
            csv_file = validated_data.get('csv_file')
            decoded_file = csv_file.read().decode('utf-8')
            io_strings = io.StringIO(decoded_file)
            csvf = csv.reader(io_strings)
            for row in csvf:
                try:
                    user = User(sid=row[0], email=row[1], full_name=row[2],
                                sex=row[3], cid=row[4], phone=row[5], date_of_birth=datetime.strptime(row[6], '%d-%m-%Y'), teacher=True)
                    user.password = make_password("freepassword")
                    user.save()
                    newEmail = EmailAddress(
                        user=user, email=row[1], verified=True)
                    newEmail.save()
                except:
                    continue
        return super().create(validated_data)
