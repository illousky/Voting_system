# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: Ignacio González Porras (github.com/illousky)

from django.shortcuts import redirect, render
from votoAppRPCClient.forms import VotoForm, CensoForm, DelVotoForm, GetVotosForm
from votoAppRPCClient.votoDB import (verificar_censo, registrar_voto,
                            eliminar_voto, get_votos_from_db)

TITLE = '(votoSite)'

# Create your views here.

def aportarinfo_voto(request):
    """
        View to handle the voting process.
        This view allows users to submit their vote after verifying their
        registration in the census.
        It checks if the user is registered in the census and then allows them
        to submit their vote. If the user is not registered, it returns an error
        message. If the vote is successfully registered, it displays a success
        message with the vote details.
        
        params:
            request: The HTTP request object containing the user's input.
        returns:
            Rendered HTML response with the voting form or success message.
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
        This view allows users to check if they are registered in the census
        before they can vote. If the user is not registered, it returns an error
        message. If the user is registered, it stores their DNI in the session
        and redirects them to the voting form.
        
        params:
            request: The HTTP request object containing the user's input.
        returns:
            Rendered HTML response with the census form or error message.
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
        View to test the database operations related to voting.
        This view allows users to submit a vote, delete a vote, or retrieve votes
        from the database. It handles both GET and POST requests for different
        functionalities.
        
        params:
            request: The HTTP request object containing the user's input.
        returns:
            Rendered HTML response with the voting form, deletion form,
            retrieval form, or success/error messages.
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
        This view allows users to delete a vote by providing the vote ID.
        If the deletion is successful, it displays a success message.
        If there is an error during deletion, it displays an error message.
        
        params:
            request: The HTTP request object containing the user's input.
        returns:
            Rendered HTML response with success or error messages.
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
        This view allows users to get votes associated with a specific electoral process.
        It handles both GET and POST requests for retrieving votes.
        
        params:
            request: The HTTP request object containing the user's input.
        returns:
            Rendered HTML response with the retrieved votes or an error message.
    """
    
    if request.method == 'POST':
        get_votos_form = GetVotosForm(request.POST)
        if get_votos_form.is_valid():
            idProcesoElectoral =\
                get_votos_form.cleaned_data['idProcesoElectoral']
            votos = get_votos_from_db(idProcesoElectoral)
            return render(request, 'template_get_votos_result.html',
                          {'result': votos, 'title': TITLE})