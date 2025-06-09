from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializers, VotoSerializer, CensoSerializer, ProcesoElectoralSerializer
from .models import Post, Censo, Voto, ProcesoElectoral
from rest_framework import status
from django.http import Http404

class Post_APIView(APIView):
    
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
    
    def get(self, request, idProcesoElectoral, format=None):
        
        proceso = Voto.objects.filter(idProcesoElectoral=idProcesoElectoral)
        
        if not proceso:
            return Response({'message': 'Proceso electoral no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VotoSerializer(proceso, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)