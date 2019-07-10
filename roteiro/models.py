from datetime import datetime, date

import requests
from django.db import models


class Localizacao(models.Model):

    latitude = models.FloatField()
    longitude = models.FloatField()


class Passeio(models.Model):

    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=150)
    duracao = models.IntegerField()
    dia = models.DateField()
    horario = models.TimeField()
    localizacao = models.ForeignKey(Localizacao, on_delete=models.CASCADE,
                                    null=True, blank=True)

    def __str__(self):
        return self.nome


class Roteiro(models.Model):

    data_de_chegada = models.DateField()
    data_de_saida = models.DateField()
    numero_de_pessoas = models.IntegerField()
    passeios = models.ManyToManyField(Passeio, blank=True)

    def escalona_passeios(self, ids):
        self.save()
        agenda = {}

        # ids_agrupados = self.agrupa_por_localizacao(ids)

        passeios_bonitour = self.consulta_passeios_bonitour()
        for id in ids:
            agendamento = self.busca_horario_disponivel(id)
            if agendamento.__len__() > 0:
                self.add_passeio(id, agendamento, passeios_bonitour)
                agenda[id] = agendamento
            else:
                agenda[id] = "nao foi possivel adicionar o passeio, horarios indisponiveis"

        return agenda


    def busca_horario_disponivel(self, id):
        disp = self.consulta_horarios_bonitour(id)

        for dia in disp:
            for horarios in list(dia.values()):
                for hora in horarios:
                    numero_de_vagas = list(hora.values())[0]
                    if (numero_de_vagas >= self.numero_de_pessoas and not
                            self.verifica_conflito_de_horario(list(dia.keys())[0], list(hora.keys())[0])):
                        return{
                            "dia": list(dia.keys())[0],
                            "horario": list(hora.keys())[0]
                        }

        return []

    def verifica_conflito_de_horario(self, dia, hora):
        hora = datetime.strptime(hora, '%H:%M').time()
        dia = datetime.strptime(dia, '%Y-%m-%d').date()
        for p in self.passeios.all():
            delta_t = datetime.combine(date(1, 1, 1), p.horario) - datetime.combine(date(1, 1, 1), hora)
            delta_t = delta_t.total_seconds()/60
            if p.dia == dia and p.duracao >= delta_t.__abs__():
                return True
        return False

    def add_passeio(self, id, horario, passeios_bonitour):

        for d in passeios_bonitour:
            if d['id'] == id:
                p = Passeio()
                p.id = d['id']
                p.nome = d['name']
                p.duracao = d['duration']
                l = Localizacao(latitude=d['location']['lat'], longitude=d['location']['long'])
                l.save()
                p.localizacao = l
                p.dia = horario['dia']
                p.horario = horario['horario']
                p.save()
                self.save()
                self.passeios.add(p)

    def consulta_horarios_bonitour(self, id):
        url = "https://bonitour-test-api.herokuapp.com/attractions/" \
              "{}?start_date={}&end_date={}".format(id, self.data_de_chegada, self.data_de_saida)
        r = requests.get(url)
        return r.json()['availability']

    def consulta_passeios_bonitour(self):
        url = "https://bonitour-test-api.herokuapp.com/attractions"
        r = requests.get(url)
        lista_de_passeios = r.json()['attractions']
        return lista_de_passeios