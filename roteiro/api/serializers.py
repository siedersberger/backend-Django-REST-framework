from rest_framework.serializers import ModelSerializer
from roteiro.models import Roteiro
from passeios.models import Passeio, Localizacao
from passeios.api.serializers import PasseioSerializer


class RoteiroSerializer(ModelSerializer):
    passeios = PasseioSerializer(many=True)

    class Meta:
        model = Roteiro
        fields = (
            'id', 'data_de_chegada', 'data_de_saida', 'numero_de_pessoas', 'passeios',
        )

    def create(self, validated_data):

        passeios = validated_data.pop('passeios')
        roteiro = Roteiro.objects.create(**validated_data)

        for p in passeios:
            p = dict(p)
            roteiro.passeios.add(Passeio.objects.get(nome=p['nome']))

        roteiro.save()

        return roteiro
