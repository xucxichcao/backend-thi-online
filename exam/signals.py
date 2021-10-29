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
        cauhoi = dict()
        questionID = 0
        sl = 0
        i = 0
        dapan = -1
        for row in csv_file:
            if(sl == 0):
                questionID = questionID+1
                cauhoi['de'] = row[1]
                sl = row[0]
            elif (sl != 0 and i != sl):
                i = i+1
                cauhoi['dapan' + str(i)] = row[0]
                if row[1].lower() == "x":
                    dapan = i
            elif(i == sl - 1):
                i = 0
                sl = 0
                if row[1].lower() == "x":
                    dapan = sl
                cauhoi['dapan' + str(sl)] = row[0]
            newCTDT = ChiTietDeThi(questionID=questionID,
                                   deThi=instance, noiDung=json.dumps(cauhoi), dapAn=dapan)
            newCTDT.save()
            cauhoi = dict()

        phongThi = PhongThi.objects.get(pk=instance.id)
        phongThi.update(deThi=instance)


@receiver(post_save, sender=PhongThi)
def taoPhongThi(sender, instance, created, **kwargs):
    if created:
        csv_file = instance.file
        for row in csv_file:
            user = User.objects.get(email=row[0])
            sinhvien = user.svinfo
            newDiemThi = DiemThi(sinhVien=sinhvien, phongThi=instance)
            newDiemThi.save()
