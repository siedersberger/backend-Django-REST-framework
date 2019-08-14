from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from roteiro.api.viewsets import RoteiroViewSet
from passeios.api.viewsets import PasseioViewSet

router = routers.DefaultRouter()
router.register(r'roteiros', RoteiroViewSet, base_name='roteiros')
router.register(r'passeios', PasseioViewSet, base_name='Passeio')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
