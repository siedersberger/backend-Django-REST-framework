import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import RoteiroSerializer
from roteiro.models import Roteiro, Reserva
from passeios.models import Passeio
from .services import escalona_passeios, formata_agenda


class RoteiroViewSet(ModelViewSet):

    serializer_class = RoteiroSerializer
    queryset = Roteiro.objects.all()

    def create(self, request, *args, **kwargs):
        """
              Função reescrita para manipulação dos dados recebidos.
              A manipulação consiste no escalonamento dos passeios.
              """
        dados = request.data

        disponibilidade_passeios = self.get_horarios_disponiveis(dados)
        agenda = escalona_passeios(disponibilidade_passeios)
        roteiro = formata_agenda(agenda.copy(), dados)

        serializer = self.serializer_class(data=roteiro)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            saida = serializer.data
            saida['reservas'] = agenda
            return Response(saida, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_horarios_disponiveis(self, dados):

        dias = []
        start_date = datetime.datetime.strptime(dados['data_de_chegada'], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(dados['data_de_saida'], '%Y-%m-%d')
        delta_t = end_date - start_date
        ids = dados['passeios']

        for cont in range(delta_t.days + 1):
            dias.append((start_date + datetime.timedelta(days=cont)))

        todos_passeios = {}
        for id in ids:
            todos_passeios[id] = {}
            passeio = Passeio.objects.get(id=id)
            disponibilidades = passeio.disponibilidade.all()
            disp = {}
            for dia in dias:
                chave_dia = dia.strftime("%Y-%m-%d")
                dia_da_semana = dia.strftime('%a').lower()
                disp[chave_dia] = []
                for hora in disponibilidades:
                    if self.verifica_vagas(dia, hora.horario, dados['numero_de_pessoas'], passeio):
                        if dia_da_semana == 'sun' and hora.sun:
                            disp[chave_dia].append(hora.horario)
                        if dia_da_semana == 'mon' and hora.mon:
                            disp[chave_dia].append(hora.horario)
                        if dia_da_semana == 'tue' and hora.tue:
                            disp[chave_dia].append(hora.horario)
                        if dia_da_semana == 'wed' and hora.wed:
                            disp[chave_dia].append(hora.horario)
                        if dia_da_semana == 'thu' and hora.thu:
                            disp[chave_dia].append(hora.horario)
                        if dia_da_semana == 'fri' and hora.fri:
                            disp[chave_dia].append(hora.horario)
                        if dia_da_semana == 'sat' and hora.sat:
                            disp[chave_dia].append(hora.horario)
            todos_passeios[id]['disponibilidade'] = disp
            todos_passeios[id]['duracao'] = passeio.duracao

        return todos_passeios

    def verifica_vagas(self, dia, horario, n_pessoas, passeio):

        reservas = Reserva.objects.filter(dia=dia, horario=horario, passeio=passeio.pk)

        soma = 0
        for r in reservas:
            roteiro = Roteiro.objects.get(pk=r.roteiro.pk)
            soma += roteiro.numero_de_pessoas

        vagas_disponiveis = passeio.numero_de_vagas - soma
        if vagas_disponiveis < n_pessoas:
            return False

        return True


