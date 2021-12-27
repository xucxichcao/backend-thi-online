from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import gvThemDeThi, gvCTDT, gvViewAllDiem, gvViewPhongThi, schoolViewAllDiem, schoolViewPhongThi, svCTDT, svViewGetDeThi, svViewGetKeyDeThi, svViewLamBai, svViewListPhongThi

router = DefaultRouter()
router.register("sv/phong-thi", svViewListPhongThi, basename="svViewPhongThi")
router.register("sv/get-de-thi", svViewGetDeThi,
                basename="Sinh viên nhận đề thi")
router.register("sv/ctdt", svCTDT, basename="Sinh viên nhận chi tiết đề thi")
router.register("sv/get-key", svViewGetKeyDeThi,
                basename="Sinh viên nhận key lấy CTĐT")
router.register("sv/lam-bai", svViewLamBai, basename="Sinh viên làm bài thi")
router.register("gv/phong-thi", gvViewPhongThi,
                basename="Giang Vien Phong Thi")
router.register("gv/de-thi", gvThemDeThi, basename="gvThemDeThi")
router.register("gv/ctdt", gvCTDT, basename="GiangViengetCTDT")
router.register("gv/diem-thi", gvViewAllDiem,
                basename="Giảng viên xem điểm 1 phòng thi")
router.register("school/phong-thi", schoolViewPhongThi, basename='Trường xem danh sách phòng thi')
router.register("school/diem-thi", schoolViewAllDiem,
                basename="Trường xem điểm phòng thi")
exam_urlpatterns = [url("api/", include(router.urls))]
