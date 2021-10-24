from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import ChiTietDeThi, DeThi
import json


@receiver(post_save, sender=DeThi)
def taoDeThi(sender, instance, created, **kwargs):
    if created:
        csv_file = instance.file
        cauhoi = dict()
        sl = 0
        i = 0
        dapan = -1
        for row in csv_file:
            if(sl == 0):
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
            newCTDT = ChiTietDeThi(
                deThi=instance, noiDung=json.dumps(cauhoi), dapAn=dapan)
            cauhoi = dict()
