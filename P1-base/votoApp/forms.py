# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: Ignacio González Porras (github.com/illousky)

from django import forms


class VotoForm(forms.Form):
    """
        Form for submitting a vote.
        This form collects information about the vote, including the electoral process,
        constituency, electoral table, and the name of the candidate voted for.
        It is used in the context of a voting application to allow users to cast their votes.
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
        Form for submitting census information.
        This form collects information about the voter, including their DNI number,
        name, date of birth, and authorization code.
        It is used in the context of a voting application to register voters in the census.
    """
    
    numeroDNI = forms.CharField(label="Número de DNI", required=True)
    nombre = forms.CharField(label="Nombre", required=True)
    fechaNacimiento = forms.CharField(
        label="Fecha de Nacimiento", required=True)
    codigoAutorizacion = forms.CharField(
        label="Código de Autorización", required=True)


class DelVotoForm(forms.Form):
    """
        Form for deleting a vote.
        This form collects the ID of the vote to be deleted.
        It is used in the context of a voting application to allow users to remove their votes.
    """
    
    id = forms.CharField(label="ID del Voto", required=True)


class GetVotosForm(forms.Form):
    """
        Form for retrieving votes.
        This form collects the ID of the electoral process for which votes are to be retrieved.
        It is used in the context of a voting application to fetch votes associated with a specific electoral process.
    """
    
    idProcesoElectoral = forms.CharField(
        label='ID del Proceso Electoral', required=True)
