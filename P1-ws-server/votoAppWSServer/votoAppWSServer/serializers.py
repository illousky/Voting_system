from rest_framework import serializers
from .models import Censo, ProcesoElectoral, Voto, Post


class CensoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Censo
        fields = ['numeroDNI', 'nombre', 'fechaNacimiento', 'anioCenso', 'codigoAutorizacion']


class VotoSerializer(serializers.ModelSerializer):
    censo_id = serializers.SlugRelatedField(queryset=Censo.objects.all(), slug_field='numeroDNI', source='censo')

    class Meta:
        model = Voto
        fields = ['idCircunscripcion', 'idMesaElectoral', 'idProcesoElectoral', 
                  'nombreCandidatoVotado', 'censo_id', 'marcaTiempo']


class ProcesoElectoralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcesoElectoral
        fields = ['idProcesoElectoral', 'nombreProcesoElectoral', 'fechaInicio', 'fechaFin']
        
        
class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']