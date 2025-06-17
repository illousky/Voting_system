# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: Ignacio González Porras (github.com/illousky)

from rest_framework import serializers
from .models import Censo, ProcesoElectoral, Voto


class CensoSerializer(serializers.ModelSerializer):
    """
        Serializer for the Censo model.
        This serializer is used to convert Censo model instances into JSON format
        and vice versa. It includes fields such as numeroDNI, nombre, fechaNacimiento,
        anioCenso, and codigoAutorizacion.
    """
    
    class Meta:
        model = Censo
        fields = ['numeroDNI', 'nombre', 'fechaNacimiento', 'anioCenso', 'codigoAutorizacion']


class VotoSerializer(serializers.ModelSerializer):
    """
        Serializer for the Voto model.
        This serializer is used to convert Voto model instances into JSON format
        and vice versa. It includes fields such as idCircunscripcion, idMesaElectoral,
        idProcesoElectoral, nombreCandidatoVotado, censo, marcaTiempo, and codigoRespuesta.
    """
    
    class Meta:
        model = Voto
        fields = ['idCircunscripcion', 'idMesaElectoral', 'idProcesoElectoral', 
                  'nombreCandidatoVotado', 'censo', 'marcaTiempo', 'codigoRespuesta']


class ProcesoElectoralSerializer(serializers.ModelSerializer):
    """
        Serializer for the ProcesoElectoral model.
        This serializer is used to convert ProcesoElectoral model instances into JSON format
        and vice versa. It includes fields such as idProcesoElectoral, nombreProcesoElectoral,
        fechaInicio, and fechaFin.
    """
    
    class Meta:
        model = ProcesoElectoral
        fields = ['idProcesoElectoral', 'nombreProcesoElectoral', 'fechaInicio', 'fechaFin']