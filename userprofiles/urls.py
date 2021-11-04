from django.db.models import base
from userprofiles.views import viewProfile
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import TruongViewSet, viewProfile

router = DefaultRouter()
router.register("profile/me", viewProfile, basename="Xem profile bản thân")
router.register("profile/create", TruongViewSet,
                basename="Tạo profile cho trường")
profile_urlpatterns = [url("api/", include(router.urls))]
