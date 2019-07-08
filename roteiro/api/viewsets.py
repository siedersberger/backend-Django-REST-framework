from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import RoteiroSerializer
from roteiro.models import Roteiro


class RoteiroViewSet(ModelViewSet):

    serializer_class = RoteiroSerializer
    queryset = Roteiro.objects.all()

    def create(self, request, *args, **kwargs):

        novo_roteiro = Roteiro()
        novo_roteiro.data_de_chegada = request.data['data_de_chegada']
        novo_roteiro.data_de_saida = request.data['data_de_saida']
        novo_roteiro.numero_de_pessoas = request.data['numero_de_pessoas']

        return Response(novo_roteiro.escalona_passeios(request.data['passeios']))
