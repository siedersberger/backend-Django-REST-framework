from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import RoteiroSerializer
from roteiro.models import Roteiro
from .services import escalona_passeios

class RoteiroViewSet(ModelViewSet):

    serializer_class = RoteiroSerializer
    queryset = Roteiro.objects.all()

    def create(self, request, *args, **kwargs):

        dados = request.data
        disponibilidade = escalona_passeios(dados)

        return Response(disponibilidade)

    @action(methods=['post'], detail=True)
    def adiciona_passeio(self, request, pk=None):
        roteiro = Roteiro.objects.get(id=pk)
        return Response(roteiro.escalona_passeios(request.data['passeios']))

