from rest_framework.serializers import ModelSerializer
from roteiro.models import Roteiro, Reserva


class ReservaSerializer(ModelSerializer):

    class Meta:
        model = Reserva
        fields = ('dia', 'horario', 'passeio')


class RoteiroSerializer(ModelSerializer):
    reservas = ReservaSerializer(many=True)

    class Meta:
        model = Roteiro
        fields = (
            'id', 'data_de_chegada', 'data_de_saida', 'numero_de_pessoas', 'reservas'
        )

    def create(self, validated_data):

        reservas = validated_data.pop('reservas')
        roteiro = Roteiro.objects.create(**validated_data)

        for r in reservas:
            r = dict(r)
            reserva = Reserva.objects.create(roteiro=roteiro, **r)

        return roteiro



