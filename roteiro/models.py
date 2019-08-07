from django.db import models
from passeios.models import Passeio

class Roteiro(models.Model):

    data_de_chegada = models.DateField()
    data_de_saida = models.DateField()
    numero_de_pessoas = models.IntegerField()
    passeios = models.ManyToManyField(Passeio, blank=True)
