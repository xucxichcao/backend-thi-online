from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import AccountBulkCreateViewSet

router = DefaultRouter()
router.register("bulk-create", AccountBulkCreateViewSet, basename="bulkCreate")

account_urlpatterns = [url("api/", include(router.urls))]
