from django.test import TestCase
from .models import Roteiro, Passeio

class RoteiroTestCase(TestCase):

    def setUp(self):
        self.p = Passeio.objects.create(
            id=1,
            nome="XYZ",
            duracao=150,
            dia="2019-09-06",
            horario="09:00",
        )

        self.r = Roteiro.objects.create(
            data_de_chegada="2019-09-06",
            data_de_saida="2019-09-16",
            numero_de_pessoas=3
        )


    def test_conflito_de_horario_deve_existir(self):

        self.r.passeios.add(self.p)

        self.assertEqual(
            True, self.r.verifica_conflito_de_horario("2019-09-06", "11:00")
        )

    def test_conflito_de_horario_nao_deve_existir(self):
        self.r.passeios.add(self.p)

        self.assertEqual(
            False, self.r.verifica_conflito_de_horario("2019-09-06", "11:31")
        )
