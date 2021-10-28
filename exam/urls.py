from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import giangVienDeThi, viewListPhongThi

router = DefaultRouter()
router.register("phong-thi", viewListPhongThi, basename="svViewPhongThi")
router.register("gv-dethi", giangVienDeThi, basename="gvPhongThi")

exam_urlpatterns = [url("api/", include(router.urls))]
