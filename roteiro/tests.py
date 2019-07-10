from datetime import datetime, date
from django.test import TestCase
from .api.services import busca_horario_disponivel, define_prioridade, agrupa_por_localizacao


class RoteiroTestCase(TestCase):

    def test_sem_conflito_de_horario_com_agenda_vazia(self):

        agenda = {}
        id = 380721
        info = {
            'location': {
                'long': '-56.4938124',
                'lat': '-21.1329963'
            },
            'availability': {
                '2019-09-06': ['08:00', '10:00', '14:00']},
            'name': 'Trilha Boiadeira - Quadriciclo',
            'duration': 60
        }

        resultado_esperado = {
            "id": id,
            "nome": 'Trilha Boiadeira - Quadriciclo',
            "dia": datetime.strptime('2019-09-06', '%Y-%m-%d').date(),
            "horario": datetime.strptime('08:00', '%H:%M').time(),
            "duracao": 60,
            "localizacao": {
                'long': '-56.4938124',
                'lat': '-21.1329963'
            }
        }


        self.assertEqual(
            resultado_esperado,
            busca_horario_disponivel(info, id, agenda)
        )

    def test_com_agenda_cheia_deve_retornar_vazio(self):

        agenda = {
            380721: {
                'horario': datetime.strptime('08:00', '%H:%M').time(),
                'nome': 'Trilha Boiadeira - Quadriciclo',
                'dia': datetime.strptime('2019-09-06', '%Y-%m-%d').date(),
                'localizacao': {
                    'long': '-56.4938124',
                    'lat': '-21.1329963'
                },
                'duracao': 60,
                'id': 380721
            },
            1596: {
                'horario': datetime.strptime('10:00', '%H:%M').time(),
                'nome': 'Balneário Municipal',
                'dia': datetime.strptime('2019-09-06', '%Y-%m-%d').date(),
                'localizacao': {
                    'long': '-56.446384',
                    'lat': '-21.17367'
                },
                'duracao': 150,
                'id': 1596
            },
            1234: {
                'horario': datetime.strptime('14:00', '%H:%M').time(),
                'nome': 'Teste',
                'dia': datetime.strptime('2019-09-06', '%Y-%m-%d').date(),
                'localizacao': {
                    'long': '-56.446384',
                    'lat': '-21.17367'
                },
                'duracao': 60,
                'id': 1234
            }
        }

        id = 1111

        info = {
            'location': {
                'long': '-56.4938124',
                'lat': '-21.1329963'
            },
            'availability': {
                '2019-09-06': ['08:00', '10:00', '14:00']},
            'name': 'Teste de alocacao',
            'duration': 60
        }

        resultado_esperado = {}


        self.assertEqual(
            resultado_esperado,
            busca_horario_disponivel(info, id, agenda)
        )

    def test_com_agenda_deve_retornar_horario_disponivel(self):

        agenda = {
            380721: {
                'horario': datetime.strptime('08:00', '%H:%M').time(),
                'nome': 'Trilha Boiadeira - Quadriciclo',
                'dia': datetime.strptime('2019-09-06', '%Y-%m-%d').date(),
                'localizacao': {
                    'long': '-56.4938124',
                    'lat': '-21.1329963'
                },
                'duracao': 60,
                'id': 380721
            },
            1596: {
                'horario': datetime.strptime('10:00', '%H:%M').time(),
                'nome': 'Balneário Municipal',
                'dia': datetime.strptime('2019-09-06', '%Y-%m-%d').date(),
                'localizacao': {
                    'long': '-56.446384',
                    'lat': '-21.17367'
                },
                'duracao': 150,
                'id': 1596
            },
            1234: {
                'horario': datetime.strptime('14:00', '%H:%M').time(),
                'nome': 'Teste',
                'dia': datetime.strptime('2019-09-06', '%Y-%m-%d').date(),
                'localizacao': {
                    'long': '-56.446384',
                    'lat': '-21.17367'
                },
                'duracao': 60,
                'id': 1234
            }
        }

        id = 1111

        info = {
            'location': {
                'long': '-56.4938124',
                'lat': '-21.1329963'
            },
            'availability': {
                '2019-09-06': ['08:00', '10:00', '16:00']},
            'name': 'Teste de alocacao',
            'duration': 60
        }

        resultado_esperado = {
            "id": id,
            "nome": 'Teste de alocacao',
            "dia": datetime.strptime('2019-09-06', '%Y-%m-%d').date(),
            "horario": datetime.strptime('16:00', '%H:%M').time(),
            "duracao": 60,
            "localizacao": {
                'long': '-56.4938124',
                'lat': '-21.1329963'
            }
        }


        self.assertEqual(
            resultado_esperado,
            busca_horario_disponivel(info, id, agenda)
        )

    def test_definicao_de_prioridade(self):

        disp = {
            380721: {
                'location': {
                    'lat': '-21.1329963', 'long': '-56.4938124'
                },
                'duration': 60,
                'name': 'Trilha Boiadeira - Quadriciclo',
                'availability': {
                    '2019-09-06': [
                        '08:00', '10:00', '14:00'
                    ]
                }
            },
            1106: {
                'location': {
                    'lat': '-20.893947', 'long': '-56.530198'
                },
                'duration': 150,
                'name': 'Nascente Azul - Flutuação',
                'availability': {
                    '2019-09-06': [
                        '08:00', '09:00', '11:20',
                        '12:40', '13:20', '14:20',
                        '14:40'
                    ]
                }
            },
            1596: {
                'location': {
                    'lat': '-21.17367', 'long': '-56.446384'
                },
                'duration': 150,
                'name': 'Balneário Municipal',
                'availability': {
                    '2019-09-06': [
                        '10:00', '10:30', '12:30',
                        '14:00', '14:30'
                    ]
                }
            }
        }

        resultado_esperado = [380721, 1596, 1106]
        self.assertEqual(
            resultado_esperado,
            define_prioridade(disp)
        )

    def test_agrupamento_por_localizacao_com_dois_grupos(self):
        disp = {
            380721: {
                'location': {
                    'lat': '-2', 'long': '-2'
                },
                'duration': 60,
                'name': 'Trilha Boiadeira - Quadriciclo',
                'availability': {
                    '2019-09-06': [
                        '08:00', '10:00', '14:00'
                    ]
                }
            },
            1106: {
                'location': {
                    'lat': '-3', 'long': '-3'
                },
                'duration': 150,
                'name': 'Nascente Azul - Flutuação',
                'availability': {
                    '2019-09-06': [
                        '08:00', '09:00', '11:20',
                        '12:40', '13:20', '14:20',
                        '14:40'
                    ]
                }
            },
            1596: {
                'location': {
                    'lat': '-3', 'long': '-3'
                },
                'duration': 150,
                'name': 'Balneário Municipal',
                'availability': {
                    '2019-09-06': [
                        '10:00', '10:30', '12:30',
                        '14:00', '14:30'
                    ]
                }
            },
            1111: {
                'location': {
                    'lat': '-2', 'long': '-2'
                },
                'duration': 150,
                'name': 'Teste',
                'availability': {
                    '2019-09-06': [
                        '10:00', '10:30', '12:30',
                        '14:00', '14:30'
                    ]
                }
            }
        }

        resultado_esperado = [[1111, 380721], [1106, 1596]]
        self.assertEqual(
            resultado_esperado,
            agrupa_por_localizacao(disp)
        )