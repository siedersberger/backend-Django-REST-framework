from django.db import models


class Localizacao(models.Model):

    cidade = models.CharField(max_length=200, unique=True)
    estado = models.CharField(max_length=200)

    def __str__(self):
        return self.cidade +" - "+ self.estado


class Disponibilidade(models.Model):

    horario = models.TimeField()
    sun = models.BooleanField(default=False)
    mon = models.BooleanField(default=False)
    tue = models.BooleanField(default=False)
    wed = models.BooleanField(default=False)
    thu = models.BooleanField(default=False)
    fri = models.BooleanField(default=False)
    sat = models.BooleanField(default=False)

    def __str__(self):
        return "{}: {}{}{}{}{}{}{}".format(self.horario, self.sun, self.mon, self.tue,
                                           self.wed, self.thu, self.fri, self.sat)


class Passeio(models.Model):

    nome = models.CharField(max_length=150, unique=True)
    duracao = models.IntegerField()
    numero_de_vagas = models.IntegerField()
    localizacao = models.ForeignKey(Localizacao, on_delete=models.CASCADE)
    disponibilidade = models.ManyToManyField(Disponibilidade)

    def __str__(self):
        return self.nome




