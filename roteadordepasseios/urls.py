from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from roteiro.api.viewsets import RoteiroViewSet

router = routers.DefaultRouter()
router.register(r'roteiro', RoteiroViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
