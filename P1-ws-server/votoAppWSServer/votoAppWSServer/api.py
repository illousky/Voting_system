from django.urls import path
from votoAppWSServer.views import CensoView, VotoView, ProcesoElectoralView

urlpatterns = [
    # check if person is in "censo"
    path("censo/", CensoView.as_view(), name="censo"),
    # create "voto"
    path("voto/", VotoView.as_view(), name="voto"),
    # get list of "votos" associated with a given  idProcesoElectoral
    path ('procesoelectoral/<str:idProcesoElectoral>', ProcesoElectoralView.as_view(), name="procesoelectoral"),
    # delete "voto" with id id_voto
    path("voto/<str:id_voto>", VotoView.as_view(), name="voto"),
]
