# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: Ignacio González Porras (github.com/illousky)

from django import forms


class VotoForm(forms.Form):
    """
        Form for submitting a vote in the electoral process.
        This form collects information about the vote, including the electoral process ID,
        the constituency ID, the electoral table ID, and the name of the candidate voted for.
        It is used to register a vote in the system.
    """
    
    idProcesoElectoral = forms.CharField(
        label='ID Proceso Electoral', required=True)
    idCircunscripcion = forms.CharField(
        label='ID Circunscripcion', required=True)
    idMesaElectoral = forms.CharField(
        label='ID Mesa Electoral', required=True)
    nombreCandidatoVotado = forms.CharField(
        label='Nombre Candidato Votado', required=True)


class CensoForm(forms.Form):
    """
        Form for collecting voter information for the electoral census.
        This form collects the voter's DNI number, name, date of birth, and authorization code.
    """
    
    numeroDNI = forms.CharField(label="Número de DNI", required=True)
    nombre = forms.CharField(label="Nombre", required=True)
    fechaNacimiento = forms.CharField(
        label="Fecha de Nacimiento", required=True)
    codigoAutorizacion = forms.CharField(
        label="Código de Autorización", required=True)


class DelVotoForm(forms.Form):
    """
        Form for deleting a vote from the electoral process.
        This form collects the ID of the vote to be deleted.
    """
    
    id = forms.CharField(label="ID del Voto", required=True)


class GetVotosForm(forms.Form):
    """
        Form for retrieving votes from the electoral process.
    """
    
    idProcesoElectoral = forms.CharField(
        label='ID del Proceso Electoral', required=True)
