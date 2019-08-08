from rest_framework.serializers import ModelSerializer
from passeios.models import Passeio, Localizacao

class LocalizacaoSerializer(ModelSerializer):
    class Meta:
        model = Localizacao
        fields = ('cidade', 'estado')
        extra_kwargs = {
            'cidade': {'validators': []},
        }


class PasseioSerializer(ModelSerializer):
    localizacao = LocalizacaoSerializer()

    class Meta:
        model = Passeio
        fields = (
            'id', 'nome', 'duracao', 'dia', 'horario', 'localizacao'
        )

    def create(self, validated_data):
        dados_localizacao = validated_data.pop('localizacao')
        localizacao_obj, created = Localizacao.objects.get_or_create(**dados_localizacao)
        passeio, created = Passeio.objects.get_or_create(localizacao=localizacao_obj, **validated_data)
        return passeio
