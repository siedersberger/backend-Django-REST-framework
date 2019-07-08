from rest_framework.serializers import ModelSerializer
from roteiro.models import Roteiro, Passeio, Localizacao

class LocalizacaoSerializer(ModelSerializer):
    class Meta:
        model = Localizacao
        fields = (
            'latitude', 'longitude'
        )


class PasseioSerializer(ModelSerializer):
    localizacao = LocalizacaoSerializer()

    class Meta:
        model = Passeio
        fields = (
            'id', 'nome', 'duracao', 'dia', 'horario', 'localizacao'
        )


class RoteiroSerializer(ModelSerializer):
    passeios = PasseioSerializer(many=True)

    class Meta:
        model = Roteiro
        fields = (
            'id', 'data_de_chegada', 'data_de_saida', 'numero_de_pessoas', 'passeios'
        )
