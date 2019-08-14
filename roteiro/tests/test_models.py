from datetime import datetime
from django.test import TestCase
from ..models import Reserva, Roteiro
from passeios.models import Passeio, Disponibilidade, Localizacao


class RoteiroTestCase(TestCase):

    def create_reserva(self, dia, horario):

        disponibilidade = Disponibilidade.objects.create(
            horario=datetime.strptime(horario, '%H:%M'),
            sun=True,
            mon=True,
            tue=True,
            wed=True,
            thu=True,
            fri=True,
            sat=True
        )

        passeio = Passeio.objects.create(
            nome='Passeio Teste',
            duracao=200,
            numero_de_vagas=10,
            localizacao = Localizacao.objects.create(
                cidade='Florianopolis',
                estado='SC'
            )
        )
        passeio.disponibilidade.add(disponibilidade)

        roteiro = Roteiro.objects.create(
            data_de_chegada=datetime.strptime(dia, '%Y-%m-%d'),
            data_de_saida= datetime.strptime(dia, '%Y-%m-%d'),
            numero_de_pessoas=2
        )

        return Reserva.objects.create(
            dia=datetime.strptime(dia, '%Y-%m-%d'),
            horario=datetime.strptime(horario, '%H:%M'),
            roteiro=roteiro,
            passeio=passeio
        )

    def test_reserva_creation(self):
        r = self.create_reserva('2019-09-01', '09:00')
        self.assertEqual(r.__str__(), "Roteiro {}, {}".format(r.roteiro.pk, r.passeio))
        self.assertTrue(isinstance(r, Reserva))
