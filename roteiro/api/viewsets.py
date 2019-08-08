from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import RoteiroSerializer

from roteiro.models import Roteiro
from passeios.models import Passeio


class RoteiroViewSet(ModelViewSet):

    serializer_class = RoteiroSerializer
    queryset = Roteiro.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Função reescrita para manipulação dos dados recebidos.
        A manipulação consiste no escalonamento dos passeios.
        """
        dados = request.data
        todos_passeios = self.passeios_filter(dados['data_de_chegada'], dados['data_de_saida'], dados['passeios'])

        roteiro = {
            "data_de_chegada": dados['data_de_chegada'],
            "data_de_saida": dados['data_de_saida'],
            "numero_de_pessoas": dados['numero_de_pessoas'],
            "passeios": todos_passeios
                   }

        serializer = self.serializer_class(data=roteiro)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def passeios_filter(self, start_date, end_date, ids):

        todos_passeios = []
        for id in ids:
            queryset = Passeio.objects.filter(dia__gte=start_date, dia__lte=end_date, id=id)
            passeio = list(queryset)[0]
            p = {
                "id": passeio.pk,
                "nome": passeio.nome,
                "duracao": passeio.duracao,
                "dia": passeio.dia,
                "horario": passeio.horario,
                "localizacao": {
                    "cidade": passeio.localizacao.cidade,
                    "estado": passeio.localizacao.estado
                }
            }
            todos_passeios.append(p)

        return todos_passeios
