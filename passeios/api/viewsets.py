import datetime
from rest_framework.viewsets import ModelViewSet
from passeios.models import Passeio
from .serializers import PasseioSerializer


class PasseioViewSet(ModelViewSet):

    serializer_class = PasseioSerializer
    queryset = Passeio.objects.all()

