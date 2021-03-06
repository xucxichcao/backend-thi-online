import io
import datetime
import json
import os
import zipfile
import csv
from rest_framework.decorators import api_view, permission_classes
import unidecode
from django.http.response import Http404, JsonResponse
from xlsxwriter.workbook import Workbook
from accounts.views import IsSchoolAccount
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import mixins, viewsets, permissions, status, renderers
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from .models import DeThi, DiemThi, DiemTuLuan, PhongThi, ChiTietDeThi
from .serializers import DiemAll, gvBaiThiTuLuan, gvGetDeTuLuan, gvPhongThi, gvSerializerUploadTuLuan, gvThemDeThiSer, schoolPhongThi, svGetDeThiTuLuan, svGetDiem, svGetKeyDeThi, gvGetChiTietDeThi, svGetChiTietDeThi, svGetListPhongThi, svGetDeThi, svLamBaiThi, svLamBaiThiTuLuan

# Renderers


class PassthroughRenderer(renderers.BaseRenderer):
    """
        Return data as-is. View should supply a Response.
    """
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    format = 'xlsx'

    def render(self, data, media_type=None, renderer_context=None):
        return data


# Permission


class isGiangVien(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.teacher


class isSinhVienAndReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.student
        return False


class isSinhVien(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.student

    def has_object_permission(self, request, view, obj):
        return request.user.student


class isGiangVienAndOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.teacher

    def has_object_permission(self, request, view, obj):
        return obj.deThi.createdBy.user == request.user


class isOwnedDeThi(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.createdBy.user == request.user


class isOwnedPhongThi(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.giangVien.user == request.user

# Create your views here.


class svViewListPhongThi(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (permissions.IsAuthenticated, isSinhVienAndReadOnly)
    serializer_class = svGetListPhongThi

    def get_queryset(self):
        user = self.request.user
        tree = self.request.query_params.get('tree')
        namHoc = self.request.query_params.get('namHoc')
        hocKi = self.request.query_params.get('hocKi')
        if tree is not None:
            return PhongThi.objects.filter(diemthi__sinhVien__user=user).distinct('namHoc')
        if namHoc is not None and hocKi is None:
            return PhongThi.objects.filter(diemthi__sinhVien__user=user, namHoc=namHoc).distinct('hocKi')
        if namHoc is not None and hocKi is not None:
            return PhongThi.objects.filter(diemthi__sinhVien__user=user, namHoc=namHoc, hocKi=hocKi)
        return PhongThi.objects.filter(diemthi__sinhVien__user=user)


class svViewGetDeThi(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated, isSinhVienAndReadOnly, )
    serializer_class = svGetDeThi

    def get_queryset(self):
        idPhongThi = self.request.query_params.get('idPhongThi')
        if idPhongThi:
            return DeThi.objects.filter(phongthi__id=idPhongThi, phongthi__diemthi__sinhVien__user=self.request.user)
        else:
            return DeThi.objects.none()


class svViewGetKeyDeThi(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated, isSinhVienAndReadOnly, )
    serializer_class = svGetKeyDeThi

    def get_queryset(self):
        idPhongThi = self.request.query_params.get('idPhongThi')
        if idPhongThi:
            return DeThi.objects.filter(phongthi__thoiGianThi__lte=datetime.datetime.now(), phongthi__id=idPhongThi)
        else:
            return DeThi.objects.none()


class svViewGetDeThiTuLuan(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated, isSinhVienAndReadOnly, )
    serializer_class = svGetDeThiTuLuan

    def get_queryset(self):
        idPhongThi = self.request.query_params.get('idPhongThi')
        key = self.request.query_params.get('key')
        if idPhongThi and key:
            return DeThi.objects.filter(phongthi__id=idPhongThi, key=key)
        else:
            return DeThi.objects.none()


class svCTDT(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = svGetChiTietDeThi
    permission_classes = (permissions.IsAuthenticated, isSinhVienAndReadOnly, )

    def get_queryset(self):
        key = self.request.query_params.get('key')
        if key:
            return ChiTietDeThi.objects.filter(deThi__key=key)
        else:
            return ChiTietDeThi.objects.none()


class svViewDiem(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = svGetDiem
    permission_classes = (permissions.IsAuthenticated, isSinhVienAndReadOnly, )

    def get_queryset(self):
        idPhongThi = self.request.query_params.get('idPhongThi')
        if idPhongThi:
            user = self.request.user
            return DiemThi.objects.filter(sinhVien__user=user, phongThi__id=idPhongThi)
        else:
            return DiemThi.objects.none()


class svViewLamBai(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = svLamBaiThi
    permission_classes = (permissions.IsAuthenticated, isSinhVien,)
    queryset = DiemThi.objects.none()

    def put(self, request, *args, **kwargs):
        idPhongThi = self.request.data['phongThi']
        kieuThi = PhongThi.objects.filter(id=idPhongThi).first().deThi.kieuThi
        if idPhongThi and kieuThi:
            user = self.request.user
            if DiemThi.objects.filter(sinhVien__user=user, phongThi__id=idPhongThi).exists():
                instance = DiemThi.objects.get(
                    phongThi__id=idPhongThi, sinhVien__user=user)
                pt = instance.phongThi
                time = pt.thoiGianThi
                timeplus = pt.thoiGianLamBai
                now = timezone.now()
                if now > time and now < (time + datetime.timedelta(minutes=timeplus)):
                    serializer = self.get_serializer(
                        instance, data=request.data, partial=False)
                    serializer.is_valid(raise_exception=True)
                    self.perform_update(serializer)
                    return Response(serializer.data)
                else:
                    return Response({"message": "Kh??ng trong th???i gian l??m b??i"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'message': 'B???n kh??ng trong ph??ng thi n??y'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Ph??ng thi kh??ng t???n t???i ho???c ????y l?? b??i thi tr???c nghi???m"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        baiLam = serializer.validated_data['baiLam']
        baiLamDict = json.loads(baiLam)
        de = ChiTietDeThi.objects.filter(
            deThi__id=serializer.validated_data['phongThi'].id)
        slch = de.count()
        dsch = de.values()
        dung = 0
        for lam in baiLamDict:
            cauhoi = next(
                (item for item in dsch if item['questionID'] == lam['questionID']), None)
            if lam['luachon'] == cauhoi['dapAn']:
                dung = dung+1
        diem = (dung/slch) * 10
        format_diem = "{:.2f}".format(diem)
        serializer.save(diem=format_diem)


class svViewLambaiTuluan(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = svLamBaiThiTuLuan
    permission_classes = (permissions.IsAuthenticated, isSinhVien, )
    queryset = DiemThi.objects.none()

    def put(self, request, *args, **kwargs):
        idPhongThi = self.request.data['phongThi']
        kieuThi = PhongThi.objects.filter(id=idPhongThi).first().deThi.kieuThi
        if idPhongThi and not kieuThi:
            user = self.request.user
            if DiemThi.objects.filter(sinhVien__user=user, phongThi__id=idPhongThi).exists():
                instance = DiemThi.objects.get(
                    phongThi__id=idPhongThi, sinhVien__user=user)
                pt = instance.phongThi
                time = pt.thoiGianThi
                timeplus = pt.thoiGianLamBai
                now = timezone.now()
                if now > time and now < (time + datetime.timedelta(minutes=timeplus)):
                    serializer = self.get_serializer(
                        instance, data=request.data, partial=False)
                    serializer.is_valid(raise_exception=True)
                    self.perform_update(serializer)
                    return Response(serializer.data)
                else:
                    return Response({"message": "Kh??ng trong th???i gian l??m b??i"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'message': 'B???n kh??ng trong ph??ng thi n??y'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Ph??ng thi kh??ng t???n t???i ho???c ????y l?? b??i thi t??? lu???n"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()


class gvViewPhongThi(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, isGiangVien, )
    serializer_class = gvPhongThi

    def perform_create(self, serializer):
        serializer.validated_data['giangVien'] = self.request.user.gvinfo
        return super().perform_create(serializer)

    def get_queryset(self):
        user = self.request.user
        tree = self.request.query_params.get('tree')
        namHoc = self.request.query_params.get('namHoc')
        hocKi = self.request.query_params.get('hocKi')
        if tree is not None:
            return PhongThi.objects.filter(giangVien__user=user).distinct('namHoc')
        if namHoc is not None and hocKi is None:
            return PhongThi.objects.filter(giangVien__user=user, namHoc=namHoc).distinct('hocKi')
        if namHoc is not None and hocKi is not None:
            return PhongThi.objects.filter(giangVien__user=user, namHoc=namHoc, hocKi=hocKi)
        return PhongThi.objects.filter(giangVien__user=user)


class gvThemDeThi(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,
                          isGiangVien, isOwnedDeThi, )
    serializer_class = gvThemDeThiSer

    def get_queryset(self):
        user = self.request.user
        return DeThi.objects.filter(createdBy__user=user)

    def perform_create(self, serializer):
        serializer.validated_data['createdBy'] = self.request.user.gvinfo
        return super().perform_create(serializer)


class gvCTDT(viewsets.ModelViewSet):
    serializer_class = gvGetChiTietDeThi
    permission_classes = (permissions.IsAuthenticated, isGiangVienAndOwner, )

    def get_queryset(self):
        idPhongThi = self.request.query_params.get('idPhongThi')
        if idPhongThi:
            user = self.request.user
            return ChiTietDeThi.objects.filter(deThi__createdBy__user=user, deThi__phongthi__id=idPhongThi)
        return ChiTietDeThi.objects.none()


class gvViewDeTuLuan(viewsets.ModelViewSet):
    serializer_class = gvGetDeTuLuan
    permission_classes = (permissions.IsAuthenticated,
                          isGiangVien, isOwnedDeThi, )

    def get_queryset(self):
        idPhongThi = self.request.query_params.get('idPhongThi')
        if idPhongThi:
            user = self.request.user
            return DeThi.objects.filter(phongThi__id=idPhongThi, createdBy__user=user)
        return DeThi.objects.none()


@permission_classes((permissions.IsAuthenticated, isGiangVien,))
def getDanhSachDiemThi(request):
    idPhongThi = request.GET.get('idPhongThi')
    if idPhongThi:
        queryset = DiemThi.objects.filter(phongThi__id=idPhongThi)
        fullDiem = []
        for diem in queryset:
            fullDiem.append(
                {"sinhVien": diem.sinhVien.full_name, "diem": diem.diem})
        output = io.BytesIO()
        book = Workbook(output, {'in_memory': True})
        sheet = book.add_worksheet()
        row = 1
        column = 0
        sheet.write(0, 0, "Sinh vi??n")
        sheet.write(0, 1, "??i???m s???")
        for item in fullDiem:
            sheet.write(row, column, item['sinhVien'])
            if item['diem']:
                sheet.write(row, column+1, item['diem'])
            else:
                sheet.write(row, column+1, 0)
            row = row + 1
        book.close()
        output.seek(0)
        tenfile = unidecode.unidecode(
            PhongThi.objects.get(id=idPhongThi).tenPhongThi)
        tenfile = tenfile.replace(" ", "")
        tenfile += ".xlsx"
        response = HttpResponse(output.read(
        ), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=%s" % tenfile
        return response
    else:
        return Http404


class gvViewAllDiem(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = DiemAll
    permission_classes = (permissions.IsAuthenticated, isGiangVien,)

    def get_queryset(self):
        idPhongThi = self.request.query_params.get('idPhongThi')
        if idPhongThi:
            user = self.request.user
            return DiemThi.objects.filter(phongThi__id=idPhongThi, phongThi__giangVien__user=user)
        return DiemThi.objects.none()


class gvViewBaiLamTuLuan(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = gvBaiThiTuLuan
    permission_classes = (permissions.IsAuthenticated, isGiangVien,)

    def get_queryset(self):
        idPhongThi = self.request.query_params.get('idPhongThi')
        if idPhongThi:
            user = self.request.user
            return DiemThi.objects.filter(phongThi__id=idPhongThi, phongThi__giangVien__user=user)
        return DiemThi.objects.none()


@permission_classes((permissions.IsAuthenticated, isGiangVien,))
def getDanhSachBaiThiTuLuan(request):
    idPhongThi = request.GET.get('idPhongThi')
    if idPhongThi:
        file = []
        lsBaiThi = DiemThi.objects.filter(phongThi__id=idPhongThi)
        for item in lsBaiThi:
            if item.baiLamTuLuan.name:
                file.append({"path": item.baiLamTuLuan.path,
                            "name": item.baiLamTuLuan.name,
                             "sid": item.sinhVien.sid})
        tenfile = unidecode.unidecode(
            PhongThi.objects.get(id=idPhongThi).tenPhongThi)
        tenfile = tenfile.replace(" ", "")
        tenfile += ".zip"
        s = io.BytesIO()
        with zipfile.ZipFile(s, "w", zipfile.ZIP_DEFLATED) as zipFile:
            for item in file:
                filename = os.path.join("uploads", item["name"])
                zip_path = item["sid"] + ".pdf"
                zipFile.write(filename, zip_path)
        response = HttpResponse(
            s.getvalue(), content_type='application/x-zip-compressed')
        response['Content-Disposition'] = "attachment; filename=%s" % tenfile
        return response
    else:
        return Http404


@permission_classes((permissions.IsAuthenticated, isGiangVien,))
@api_view(['POST'])
def uploadDiemThi(request):
    idPhongThi = request.POST.get('idPhongThi')
    fileDiem = request.FILES['file']
    print(idPhongThi)
    decoded_file = fileDiem.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    csvf = csv.reader(io_string)
    for row in csvf:
        try:
            mssv = str(row[0])
            diem = row[1]
            print(mssv)
            obj = DiemThi.objects.get(
                sinhVien__sid=mssv, phongThi__id=idPhongThi)
            print(obj)
            obj.diem = diem
            obj.save()
        except:
            continue
    return JsonResponse({'message': 'Upload ??i???m th??nh c??ng', 'status': 'success'})


@permission_classes((permissions.IsAuthenticated, isGiangVien,))
@api_view(['GET'])
def downloadFileToUpload(request):
    idPhongThi = request.GET.get('idPhongThi')
    if idPhongThi:
        queryset = DiemThi.objects.filter(phongThi__id=idPhongThi)
        fullDiem = []
        for diem in queryset:
            fullDiem.append(
                {"sinhVien": diem.sinhVien.sid, "diem": 0})
        output = io.BytesIO()
        book = Workbook(output, {'in_memory': True})
        sheet = book.add_worksheet()
        row = 0
        column = 0
        for item in fullDiem:
            sheet.write(row, column, item['sinhVien'])
            sheet.write(row, column+1, item['diem'])
            row = row + 1
        book.close()
        output.seek(0)
        tenfile = unidecode.unidecode(
            PhongThi.objects.get(id=idPhongThi).tenPhongThi)
        tenfile = tenfile.replace(" ", "")
        tenfile += ".xlsx"
        tenfile = "DS-" + tenfile
        response = HttpResponse(output.read(
        ), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=%s" % tenfile
        return response
    else:
        return Http404


class schoolViewPhongThi(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = schoolPhongThi
    permission_classes = (permissions.IsAuthenticated, IsSchoolAccount, )

    def get_queryset(self):
        user = self.request.user
        tree = self.request.query_params.get('tree')
        namHoc = self.request.query_params.get('namHoc')
        hocKi = self.request.query_params.get('hocKi')
        if tree is not None:
            return PhongThi.objects.filter(giangVien__school__user=user).distinct('namHoc')
        if namHoc is not None and hocKi is None:
            return PhongThi.objects.filter(giangVien__school__user=user, namHoc=namHoc).distinct('hocKi')
        if namHoc is not None and hocKi is not None:
            return PhongThi.objects.filter(giangVien__school__user=user, namHoc=namHoc, hocKi=hocKi)
        return PhongThi.objects.filter(giangVien__school__user=user)


class schoolViewAllDiem(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = DiemAll
    permission_classes = (permissions.IsAuthenticated, IsSchoolAccount, )

    def get_queryset(self):
        idPhongThi = self.request.query_params.get('idPhongThi')
        if idPhongThi:
            user = self.request.user
            return DiemThi.objects.filter(phongThi__id=idPhongThi, phongThi__giangVien__school__user=user)
        return DiemThi.objects.none()
