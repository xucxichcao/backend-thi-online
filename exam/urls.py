from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import gvThemDeThi, gvCTDT, gvViewPhongThi, svCTDT, svViewGetKeyDeThi, svViewListPhongThi

router = DefaultRouter()
router.register("sv/phong-thi", svViewListPhongThi, basename="svViewPhongThi")
router.register("sv/ctdt", svCTDT, basename="SinhViengetCTDT")
router.register("sv/getkey", svViewGetKeyDeThi,
                basename="Sinh vien get key de thi")
router.register("gv/phong-thi", gvViewPhongThi,
                basename="Giang Vien Phong Thi")
router.register("gv/dethi", gvThemDeThi, basename="gvThemDeThi")
router.register("gv/ctdt", gvCTDT, basename="GiangViengetCTDT")
exam_urlpatterns = [url("api/", include(router.urls))]
