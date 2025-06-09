from django.urls import path
from .views import *

urlpatterns = [
    path('restapiserver/post', Post_APIView.as_view()),
    path('restapiserver/post/<int:pk>/', Post_APIView_Detail.as_view()),
    path('restapiserver/censo/', CensoView.as_view(), name='censo'),
    path('restapiserver/voto/', VotoView.as_view(), name='voto'),
    path('restapiserver/procesoelectoral/<str:idProcesoElectoral>', ProcesoElectoralView.as_view(), name='procesoelectoral'),
    path('restapiserver/voto/<str:id_voto>', VotoView.as_view(), name='voto'),
]
