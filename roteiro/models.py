from django.db import models


class Localizacao(models.Model):

    lat = models.FloatField()
    long = models.FloatField()


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