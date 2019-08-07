from rest_framework.viewsets import ModelViewSet
from passeios.models import Passeio, Localizacao
from .serializers import PasseioSerializer


class PasseioViewSet(ModelViewSet):

    serializer_class = PasseioSerializer

    def get_queryset(self):
        """Filtra passeios conforme o periodo definido nos parametros das queries (query_params).
         Sao retornados apenas os dentro do range."""
        data_chegada = self.request.query_params.get('start_date', None)
        data_saida = self.request.query_params.get('end_date', None)
        queryset = Passeio.objects.all()

        if data_chegada:
            queryset = queryset.filter(dia__gt=data_chegada)

        if data_saida:
            queryset = queryset.filter(dia__lte=data_saida)

        return queryset

