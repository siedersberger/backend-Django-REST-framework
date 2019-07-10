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
        """
        Função reescrita para manipulação dos dados recebidos.
        A manipulação consiste no escalonamento dos passeios.
        """
        dados = request.data
        todos_passeios = escalona_passeios(dados)
        passeios_escalonados = [passeio for passeio in todos_passeios if passeio.items().__len__() > 4]

        roteiro = {
            "data_de_chegada": dados['data_de_chegada'],
            "data_de_saida": dados['data_de_saida'],
            "numero_de_pessoas": dados['numero_de_pessoas'],
            "passeios": passeios_escalonados
                   }

        serializer = self.serializer_class(data=roteiro)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(todos_passeios)

