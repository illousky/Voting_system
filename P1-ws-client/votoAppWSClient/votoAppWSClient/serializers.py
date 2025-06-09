from rest_framework import serializers
from .models import Censo, ProcesoElectoral, Voto


class CensoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Censo
        fields = ['numeroDNI', 'nombre', 'fechaNacimiento', 'anioCenso', 'codigoAutorizacion']


class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = ['idCircunscripcion', 'idMesaElectoral', 'idProcesoElectoral', 
                  'nombreCandidatoVotado', 'censo', 'marcaTiempo', 'codigoRespuesta']


class ProcesoElectoralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcesoElectoral
        fields = ['idProcesoElectoral', 'nombreProcesoElectoral', 'fechaInicio', 'fechaFin']