from django.db.models import base
from userprofiles.views import viewProfile
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import viewProfile

router = DefaultRouter()
router.register("profile/me", viewProfile, basename="Xem profile bản thân")
profile_urlpatterns = [url("api/", include(router.urls))]
