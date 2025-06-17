# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: Ignacio González Porras (github.com/illousky)

from rest_framework import serializers
from .models import Censo, ProcesoElectoral, Voto, Post


class CensoSerializer(serializers.ModelSerializer):
    """
        Serializer for the Censo model, which includes fields for
        the voter's DNI number, name, birth date, census year, and authorization code.
        It uses SlugRelatedField to represent the 'numeroDNI' as a slug field.
    """
    
    class Meta:
        model = Censo
        fields = ['numeroDNI', 'nombre', 'fechaNacimiento', 'anioCenso', 'codigoAutorizacion']


class VotoSerializer(serializers.ModelSerializer):
    """
        Serializer for the Voto model, which includes fields for
        the electoral process ID, electoral district ID, electoral table ID,
        the name of the candidate voted for, the timestamp of the vote,
        and a reference to the Censo model using SlugRelatedField.
    """
    
    censo_id = serializers.SlugRelatedField(queryset=Censo.objects.all(), slug_field='numeroDNI', source='censo')

    class Meta:
        model = Voto
        fields = ['idCircunscripcion', 'idMesaElectoral', 'idProcesoElectoral', 
                  'nombreCandidatoVotado', 'censo_id', 'marcaTiempo']


class ProcesoElectoralSerializer(serializers.ModelSerializer):
    """
        Serializer for the ProcesoElectoral model, which includes fields for
        the electoral process ID, name, start date, and end date.
        It uses SlugRelatedField to represent the 'idProcesoElectoral' as a slug field.
    """
    
    class Meta:
        model = ProcesoElectoral
        fields = ['idProcesoElectoral', 'nombreProcesoElectoral', 'fechaInicio', 'fechaFin']
        
        
class PostSerializers(serializers.ModelSerializer):
    """
        Serializer for the Post model, which includes fields for
        the title and content of the post.
        It is used to serialize and deserialize Post instances.
    """
    
    class Meta:
        model = Post
        fields = ['title', 'content']