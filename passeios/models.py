from django.db import models


class Localizacao(models.Model):

    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)

    def __str__(self):
        return self.cidade +" - "+ self.estado

class Passeio(models.Model):

    nome = models.CharField(max_length=150)
    duracao = models.IntegerField()
    dia = models.DateField()
    horario = models.TimeField()
    localizacao = models.ForeignKey(Localizacao, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome