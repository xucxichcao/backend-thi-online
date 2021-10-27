from rest_framework import serializers
import csv
import io
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from allauth.account.models import EmailAddress
from accounts.models import CustomUser, accountBulkCreate
from userprofiles.models import SinhVien, GiangVien


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'role']


class AccountBulkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountBulkCreate
        fields = ('user', 'csv_file', 'type')

    def create(self, validated_data):
        school = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            school = request.user.scinfo
        accType = validated_data.get('type')
        if(accType == 'S'):
            csv_file = validated_data.get('csv_file')
            decoded_file = csv_file.read().decode('utf-8')
            io_strings = io.StringIO(decoded_file)
            csvf = csv.reader(io_strings)
            for row in csvf:
                try:
                    user = User(email=row[1], student=True)
                    user.password = make_password(row[3])
                    user.save()
                    newSinhVien = SinhVien(
                        user=user, full_name=row[2], sex=row[4], cid=row[5], phone=row[6], date_of_birth=datetime.strptime(row[7], '%d-%m-%Y'), school=school)
                    newSinhVien.save()
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
                    user = User(email=row[1], student=True)
                    user.password = make_password(row[3])
                    user.save()
                    newGiangVien = GiangVien(
                        user=user, full_name=row[2], sex=row[4], cid=row[5], phone=row[6], date_of_birth=datetime.strptime(row[7], '%d-%m-%Y'), school=school)
                    newGiangVien.save()
                    newEmail = EmailAddress(
                        user=user, email=row[1], verified=True)
                    newEmail.save()
                except:
                    continue
        return super().create(validated_data)
