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

    def cria_passeios(self, passeios, roteiro):
        for passeio in passeios:

            passeio = dict(passeio)
            local = passeio['localizacao']
            del passeio['localizacao']

            p, created = Passeio.objects.get_or_create(**passeio)
            if created:
                l = Localizacao.objects.create(**local)
                p.localizacao = l
                p.save()
                roteiro.passeios.add(p)
            else:
                roteiro.passeios.add(p)

    def create(self, validated_data):

        passeios = validated_data['passeios']
        del validated_data['passeios']

        roteiro = Roteiro.objects.create(**validated_data)
        self.cria_passeios(passeios, roteiro)

        roteiro.save()

        return roteiro
