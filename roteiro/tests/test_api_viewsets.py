import json

from datetime import datetime
from django.urls import reverse
from rest_framework import status
from django.test import TestCase, Client
from passeios.models import Passeio, Localizacao, Disponibilidade
from ..models import Roteiro, Reserva
from ..api.serializers import RoteiroSerializer

client = Client()


class TestGetRoteiros(TestCase):

    def setUp(self):
        passeio = Passeio.objects.create(
            nome='Passeio Teste',
            duracao=200,
            numero_de_vagas=10,
            localizacao=Localizacao.objects.create(
                cidade='Florianopolis',
                estado='SC'
            )
        )
        passeio.disponibilidade.add(
            Disponibilidade.objects.create(
                horario=datetime.strptime('09:00', '%H:%M'),
                sun=True,
                mon=True,
                tue=True,
                wed=True,
                thu=True,
                fri=True,
                sat=True
            )
        )
        self.roteiro = Roteiro.objects.create(
            data_de_chegada=datetime.strptime('2019-09-01', '%Y-%m-%d'),
            data_de_saida=datetime.strptime('2019-09-01', '%Y-%m-%d'),
            numero_de_pessoas=2
        )
        Reserva.objects.create(
            dia=datetime.strptime('2019-09-01', '%Y-%m-%d'),
            horario=datetime.strptime('09:00', '%H:%M'),
            roteiro=self.roteiro,
            passeio=passeio
        )

    def test_get_all_roteiros(self):
        response = client.get(reverse('roteiros-list'))
        roteiros = Roteiro.objects.all()
        serializer = RoteiroSerializer(roteiros, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_roteiro(self):
        response = client.get(reverse('roteiros-detail', kwargs={'pk': self.roteiro.pk}))
        roteiro = Roteiro.objects.get(pk=self.roteiro.pk)
        serializer = RoteiroSerializer(roteiro)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_roteiro(self):
        response = client.get(reverse('roteiros-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestCreateRoteiros(TestCase):

    def setUp(self):
        self.passeio = Passeio.objects.create(
            nome='Passeio Teste',
            duracao=200,
            numero_de_vagas=10,
            localizacao=Localizacao.objects.create(
                cidade='Florianopolis',
                estado='SC'
            )
        )
        self.passeio.disponibilidade.add(
            Disponibilidade.objects.create(
                horario=datetime.strptime('09:00', '%H:%M'),
                sun=True,
                mon=True,
                tue=True,
                wed=True,
                thu=True,
                fri=True,
                sat=True
            )
        )
        self.valid_payload = {
            'data_de_chegada': '2019-09-01',
            'data_de_saida': '2019-09-01',
            'numero_de_pessoas': 3,
            'passeios': [
                self.passeio.pk
            ]
        }
        self.invalid_payload = {
            'data_de_chegada': '2019-09-01',
            'data_de_saida': '2019-09-01',
            'numero_de_pessoas': 3,
            'passeios': [
                30
            ]
        }

    def test_create_valid_roteiro(self):
        response = client.post(
            reverse('roteiros-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)