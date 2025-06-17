# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: Ignacio González Porras (github.com/illousky)

from django.shortcuts import redirect, render
from votoApp.forms import VotoForm, CensoForm, DelVotoForm, GetVotosForm
from votoApp.votoDB import (verificar_censo, registrar_voto,
                            eliminar_voto, get_votos_from_db)
import socket

TITLE = '(votoSite)'

# Create your views here.

def aportarinfo_voto(request):
    """
        View to handle the voting process.
        It checks if the user is registered in the census.
        If the user is not registered, it displays an error message.
        If the user is registered, it allows them to vote.
        
        params:
            request: HttpRequest object containing the request data.
        Returns:
            HttpResponse object rendering the voting form or success message.
    """
    
    if request.method == 'POST':
        # data from form
        voto_form = VotoForm(request.POST)
        voto_form.get_context()

        # recoger variable de session

        if 'numeroDNI' in request.session:
            numeroDNI = request.session['numeroDNI']
        else:
            return render(
                request, 'template_mensaje.html',
                {'mensaje': '¡Error: DNI no encontrado en la sesión!',
                 'title': TITLE})
        voto_data = voto_form.cleaned_data
        # add numeroDNI to data
        voto_data['censo_id'] = numeroDNI
        voto_data['instancia'] = socket.gethostname()
        # save voto and get updated voto
        voto = registrar_voto(voto_data)
        if voto is None:
            return render(request, 'template_mensaje.html',
                          {'mensaje': '¡Error: al registrar voto!',
                           'title': TITLE})
        context_dict = {'voto': voto, 'title': TITLE}
        return render(request, 'template_exito.html', context_dict)
    else:
        voto_form = VotoForm()
        context_dict = {'form': voto_form, 'title': TITLE}
        return render(request, 'template_voto.html', context_dict)


def aportarinfo_censo(request):
    """
        View to handle the census comprobation process.
        It checks if the user is registered in the census.
        If the user is not registered, it displays an error message.
        If the user is registered, it redirects them to the voting form.
        
        params:
            request: HttpRequest object containing the request data.
        Returns:
            HttpResponse object rendering the voting form or error message.
    """

    if request.method == 'POST':

        censo_form = CensoForm(request.POST)
        censo_form.get_context()
        
        if not censo_form.is_valid():
            return render(
                request, 'template_mensaje.html',
                {'mensaje': '¡Error: Datos inválidos!',
                 'title': TITLE})

        if verificar_censo(censo_form.cleaned_data) is False:
            return render(
                request, 'template_mensaje.html',
                {'mensaje': '¡Error: Votante no registrado en el Censo!',
                 'title': TITLE})

        request.session['numeroDNI'] = censo_form.cleaned_data['numeroDNI']
        return redirect('voto')

    else:

        censo_form = CensoForm()
        context_dict = {'form': censo_form, 'title': TITLE}

        return render(request, 'template_censo.html', context_dict)


def testbd(request):
    """
        View to test the database operations.
        It allows users to register votes, delete votes, and retrieve votes.
        If the user is not registered in the census, it displays an error message.
        If the user is registered, it allows them to vote and displays success messages.
        
        params:
            request: HttpRequest object containing the request data.
        Returns:
            HttpResponse object rendering the test database form or success message.
    """

    if request.method == 'POST':

        voto_form = VotoForm(request.POST)
        censo_form = CensoForm(request.POST)
        censo_form.get_context()
        voto_form.get_context()

        if verificar_censo(censo_form.cleaned_data) is False:
            return render(
                request, 'template_mensaje.html',
                {'mensaje': '¡Error: Votante no registrado en el Censo!',
                 'title': TITLE})

        data = voto_form.cleaned_data
        data['censo_id'] = censo_form.cleaned_data['numeroDNI']
        data['instancia'] = socket.gethostname()

        # save voto

        voto = registrar_voto(data)

        if voto is None:
            return render(
                request, 'template_mensaje.html',
                {'mensaje': 'Error al registrar voto!',
                 'title': TITLE})

        context_dict = {'voto': voto, 'title': TITLE}

        return render(request, 'template_exito.html', context_dict)
    else:
        voto_form = VotoForm()
        del_voto_form = DelVotoForm()
        censo_form = CensoForm()
        get_votos_form = GetVotosForm()

        return render(request, 'template_test_bd.html',
                      {'voto_form': voto_form,
                       'censo_form': censo_form,
                       'del_voto_form': del_voto_form,
                       'get_votos_form': get_votos_form,
                       'title': TITLE})


def delvoto(request):
    """
        View to handle the deletion of votes.
        It allows users to delete votes by providing the vote ID.
        If the vote ID is valid, it deletes the vote and displays a success message.
        If the vote ID is invalid, it displays an error message.
        
        params:
            request: HttpRequest object containing the request data.
        Returns:
            HttpResponse object rendering the deletion form or success message.
    """

    if request.method == 'POST':
        del_voto_form = DelVotoForm(request.POST)
        if del_voto_form.is_valid():
            id = del_voto_form.cleaned_data['id']
            if eliminar_voto(id) is False:
                return render(request, 'template_mensaje.html',
                              {'mensaje': '¡Error: al elminar voto!',
                               'title': TITLE})
            return render(request, 'template_mensaje.html',
                          {'mensaje': '¡Voto eliminado correctamente!',
                           'title': TITLE})


def getvotos(request):
    """
        View to retrieve votes from the database.
        It allows users to get votes by providing the electoral process ID.
        If the ID is valid, it retrieves the votes and displays them.
        If the ID is invalid, it displays an error message.
        
        params:
            request: HttpRequest object containing the request data.
        Returns:
            HttpResponse object rendering the votes or error message.
    """
    
    if request.method == 'POST':
        get_votos_form = GetVotosForm(request.POST)
        if get_votos_form.is_valid():
            idProcesoElectoral =\
                get_votos_form.cleaned_data['idProcesoElectoral']
            votos = get_votos_from_db(idProcesoElectoral)
            return render(request, 'template_get_votos_result.html',
                          {'result': votos, 'title': TITLE})