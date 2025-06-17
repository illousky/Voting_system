# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: Ignacio González Porras (github.com/illousky)

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializers, VotoSerializer, CensoSerializer, ProcesoElectoralSerializer
from .models import Post, Censo, Voto, ProcesoElectoral
from rest_framework import status
from django.http import Http404

class Post_APIView(APIView):
    """
        API View for handling posts.
        This view allows for retrieving all posts and creating a new post.
        It supports GET and POST requests.
        
        Methods:
            get: Retrieves all posts and returns them in JSON format.
            post: Creates a new post with the provided data and returns the created post in JSON format.
            If the data is invalid, it returns an error response with status 400.
    """
    
    def get(self, request, format=None):
        
        post = Post.objects.all()
        serializer = PostSerializers(post, many=True)
        
        return Response(serializer.data)
    
    def post(self, request, format=None):
        
        serializer = PostSerializers(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Post_APIView_Detail(APIView):
    """
        API View for handling post details.
        This view allows for retrieving, updating, and deleting a specific post.
        It supports GET, PUT, and DELETE requests.
        
        Methods:
            get: Retrieves a specific post by its primary key (pk) and returns it in JSON format.
            put: Updates a specific post with the provided data and returns the updated post in JSON format.
                  If the data is invalid, it returns an error response with status 400.
            delete: Deletes a specific post by its primary key (pk) and returns a 204 No Content response.
    """
    
    def get_object(self, pk):
        
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        
        post = self.get_object(pk)
        serializer = PostSerializers(post)  
        
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        
        post = self.get_object(pk)
        serializer = PostSerializers(post, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        
        post = self.get_object(pk)
        post.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CensoView(APIView):
    """
        API View for handling census data.
        This view allows for checking if a voter's data exists in the census.
        It supports POST requests to verify the voter's information.
        
        Methods:
            post: Checks if the voter's data (DNI number, name, date of birth, and authorization code)
                  exists in the census. If found, it returns a success message; otherwise, it returns
                  a not found message with status 404.
    """
    
    def post(self, request, format=None):
        
        numeroDNI = request.data.get('numeroDNI')
        nombre = request.data.get('nombre')
        fechaNacimiento = request.data.get('fechaNacimiento')
        codigoAutorizacion = request.data.get('codigoAutorizacion')
        
        if Censo.objects.filter(
            numeroDNI=numeroDNI, 
            nombre=nombre, 
            fechaNacimiento=fechaNacimiento,
            codigoAutorizacion=codigoAutorizacion
        ).exists():
            
            return Response({'message': 'Datos encontrados en Censo.'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Datos no encontrados en Censo.'}, status=status.HTTP_404_NOT_FOUND)
    
    
class VotoView(APIView):
    """
        API View for handling votes in the electoral process.
        This view allows for submitting a vote, deleting a vote, and retrieving votes
        for a specific electoral process. It supports POST and DELETE requests.
        
        Methods:
            post: Submits a vote with the provided data (censo_id, idProcesoElectoral, idCircunscripcion,
                  idMesaElectoral, nombreCandidatoVotado, marcaTiempo, codigoRespuesta). If the voter's
                  data is not found in the census or if the voter has already voted in the electoral process,
                  it returns an error response. If the vote is successfully saved, it returns the vote data.
            delete: Deletes a specific vote by its ID. If the vote does not exist, it returns a not found message.
    """
    
    def post(self, request, format=None):
        
        censo_id = request.data.get('censo_id')
        idProcesoElectoral = request.data.get('idProcesoElectoral')
        idCircunscripcion = request.data.get('idCircunscripcion')
        idMesaElectoral = request.data.get('idMesaElectoral')
        candidato = request.data.get('nombreCandidatoVotado')
        tiempo = request.data.get('marcaTiempo')
        codigoRespuesta = request.data.get('codigoRespuesta')
        
        censo = Censo.objects.filter(numeroDNI=censo_id).first()
        if not censo:
            return Response({'message': 'Datos no encontrados en Censo.'}, status=status.HTTP_404_NOT_FOUND)
        
        if Voto.objects.filter(censo=censo, idProcesoElectoral=idProcesoElectoral).exists():
            return Response({'message': 'El votante ya ha emitido un voto en este proceso electoral.'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'censo_id': censo_id,
            'idProcesoElectoral': idProcesoElectoral,
            'idCircunscripcion': idCircunscripcion,
            'idMesaElectoral': idMesaElectoral,
            'nombreCandidatoVotado': candidato,
            'marcaTiempo': tiempo,
            'codigoRespuesta': codigoRespuesta
        }
        
        serializer = VotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'Davos de voto no validos.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id_voto, format=None):
        
        if not Voto.objects.filter(id=id_voto).exists():
            return Response({'message': 'Voto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        voto = Voto.objects.get(id=id_voto)
        voto.delete()
        
        return Response({'message': 'Voto eliminado'}, status=status.HTTP_200_OK)
    
    
class ProcesoElectoralView(APIView):
    """
        API View for handling electoral processes.
        This view allows for retrieving all electoral processes and creating a new electoral process.
        It supports GET and POST requests.
        
        Methods:
            get: Retrieves all electoral processes and returns them in JSON format.
    """
    
    def get(self, request, idProcesoElectoral, format=None):
        
        proceso = Voto.objects.filter(idProcesoElectoral=idProcesoElectoral)
        
        if not proceso:
            return Response({'message': 'Proceso electoral no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VotoSerializer(proceso, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)