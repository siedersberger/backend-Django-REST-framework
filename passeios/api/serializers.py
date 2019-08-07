from rest_framework.serializers import ModelSerializer
from passeios.models import Passeio, Localizacao

class LocalizacaoSerializer(ModelSerializer):
    class Meta:
        model = Localizacao
        fields = (
            'cidade', 'estado'
        )


class PasseioSerializer(ModelSerializer):
    localizacao = LocalizacaoSerializer()

    class Meta:
        model = Passeio
        fields = (
            'id', 'nome', 'duracao', 'dia', 'horario', 'localizacao'
        )