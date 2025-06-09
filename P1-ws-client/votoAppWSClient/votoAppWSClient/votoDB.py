# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: rmarabini
"Interface with the dataabse"

import requests
from django.conf import settings

api_url = settings.RESTAPIBASEURL

def verificar_censo(censo_data):
    """ Check if the voter is registered in the Censo
    :param censo_dict: dictionary with the voter data
                       (as provided by CensoForm)
    :return True or False if censo_data is not valid
    """
    try:
        response = requests.post(api_url + "censo/", json=censo_data)
        if response.status_code == 200:
            return True
        
    except Exception as e:
        print("Error: Verificando censo: ", e)
        
    return False


def registrar_voto(voto_dict):
    """ Register a vote in the database
    :param voto_dict: dictionary with the vote data (as provided by VotoForm)
      plus de censo_id (numeroDNI) of the voter
    :return new voto info if succesful, None otherwise
    """
    try:
        response = requests.post(api_url + "voto/", json=voto_dict)
        if response.status_code == 200:
            return response.json()
        
    except Exception as e:
        print("Error: Registrando voto: ", e)
        
    return None


def eliminar_voto(idVoto):
    """ Delete a vote in the database
    :param idVoto: id of the vote to be deleted
    :return True if succesful,
     False otherwise
     """
    try:
        response = requests.delete(api_url + "voto/" + str(idVoto))
        if response.status_code == 200:
            return True
        
    except Exception as e:
        print("Error: Eliminando voto: ", e)
        
    return False


def get_votos_from_db(idProcesoElectoral):
    """ Gets votes in the database correspondint to some electoral processs
    :param idProcesoElectoral: id of the vote to be deleted
    :return list of votes found
     """
    try:
        response = requests.get(api_url + "procesoelectoral/" + idProcesoElectoral)
        if response.status_code == 200:
            return response.json()
        
    except Exception as e:
        print("Error: Obteniendo votos: ", e)
        
    return None
