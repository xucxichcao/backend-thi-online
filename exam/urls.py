from exam.serializers import gvThemDeThi
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import gvThemDeThi, gvCTDT, svCTDT, svViewListPhongThi

router = DefaultRouter()
router.register("sv/phong-thi", svViewListPhongThi, basename="svViewPhongThi")
router.register("gv/dethi", gvThemDeThi, basename="gvThemDeThi")
router.register("sv/ctdt", svCTDT, basename="SinhViengetCTDT")
router.register("gv/ctdt", gvCTDT, basename="GiangViengetCTDT")
exam_urlpatterns = [url("api/", include(router.urls))]
