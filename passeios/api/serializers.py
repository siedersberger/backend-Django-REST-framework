from rest_framework.serializers import ModelSerializer
from passeios.models import Passeio, Localizacao, Disponibilidade


class LocalizacaoSerializer(ModelSerializer):

    class Meta:
        model = Localizacao
        fields = ('cidade', 'estado')
        extra_kwargs = {
            'cidade': {'validators': []},
        }


class DisponibilidadeSerializer(ModelSerializer):

    class Meta:
        model = Disponibilidade
        fields = "__all__"


class PasseioSerializer(ModelSerializer):
    localizacao = LocalizacaoSerializer()
    disponibilidade = DisponibilidadeSerializer(many=True)

    class Meta:
        model = Passeio
        fields = (
            'id', 'nome', 'duracao', 'numero_de_vagas', 'localizacao', 'disponibilidade'
        )
        extra_kwargs = {
            'nome': {'validators': []},
        }

    def create(self, validated_data):
        dados_localizacao = validated_data.pop('localizacao')
        localizacao_obj, created = Localizacao.objects.get_or_create(**dados_localizacao)
        dados_disponibilidade = validated_data.pop('disponibilidade')
        passeio, created = Passeio.objects.get_or_create(localizacao=localizacao_obj, **validated_data)

        for dados in dados_disponibilidade:
            disponibilidade_obj, created = Disponibilidade.objects.get_or_create(**dados)
            passeio.disponibilidade.add(disponibilidade_obj)

        passeio.save()
        return passeio
