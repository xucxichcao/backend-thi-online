from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import giangVienDeThi, gvCTDT, svCTDT, viewListPhongThi

router = DefaultRouter()
router.register("sv/phong-thi", viewListPhongThi, basename="svViewPhongThi")
router.register("gv/dethi", giangVienDeThi, basename="gvPhongThi")
router.register("sv/ctdt", svCTDT, basename="SinhViengetCTDT")
router.register("gv/ctdt", gvCTDT, basename="GiangViengetCTDT")
exam_urlpatterns = [url("api/", include(router.urls))]
