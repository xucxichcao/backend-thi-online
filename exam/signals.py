import csv
from io import StringIO
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import ChiTietDeThi, DeThi, DiemThi, PhongThi
import json
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=DeThi)
def taoDeThi(sender, instance, created, **kwargs):
    if created:
        csv_file = instance.file
        csvf = csv_file.read().decode('utf-8-sig')
        csv_data = csv.reader(StringIO(csvf), delimiter=',')
        cauhoi = {'cauhoi': '', 'luachon': []}
        dapan = -1
        questionID = 0
        for row in csv_data:
            print(row[0])
            slda = int(row[0])
            cauhoi['cauhoi'] = row[1]
            for i in range(slda):
                cauhoi['luachon'].append({"id": i, "noidung": row[2+i]})
            dapan = int(row[slda+2])
            newCTDT = ChiTietDeThi(questionID=questionID,
                                   deThi=instance, noiDung=json.dumps(cauhoi), dapAn=dapan)
            newCTDT.save()
            questionID = questionID+1
            cauhoi = {'cauhoi': '', 'luachon': []}

        phongThi = PhongThi.objects.get(pk=instance.id)
        phongThi.deThi = instance
        phongThi.save()


@receiver(post_save, sender=PhongThi)
def taoPhongThi(sender, instance, created, **kwargs):
    if created:
        file = instance.danhSach
        csvf = file.read().decode('utf-8-sig')
        csv_data = csv.reader(StringIO(csvf), delimiter=',')
        for row in csv_data:
            user = User.objects.get(email=row[0])
            sinhvien = user.stinfo
            newDiemThi = DiemThi(sinhVien=sinhvien, phongThi=instance)
            newDiemThi.save()
