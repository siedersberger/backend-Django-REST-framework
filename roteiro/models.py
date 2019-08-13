from django.db import models
from passeios.models import Passeio


class Roteiro(models.Model):

    data_de_chegada = models.DateField()
    data_de_saida = models.DateField()
    numero_de_pessoas = models.IntegerField()

    # @property
    # def reservas(self):
    #     return Reserva.objects.filter(roteiro=self.pk)


class Reserva(models.Model):

    dia = models.DateField()
    horario = models.TimeField()
    roteiro = models.ForeignKey(Roteiro, related_name='reservas', on_delete=models.CASCADE)
    passeio = models.ForeignKey(Passeio, related_name='reservas', on_delete=models.CASCADE)

    def __str__(self):
        return "Roteiro {}, {}".format(self.roteiro.pk, self.passeio)