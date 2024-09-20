from django.urls import path, include
from gerenciar_controle_ifto.view import pessoa,rfid,home

urlpatterns = [
    path('', home.home),
    path('cadastrarTagRfid/', rfid.cadastrarRFID),
    path('editarTagRfid/', rfid.editarRFID),
    path('listarTagRfid/', rfid.listarRFID)
]