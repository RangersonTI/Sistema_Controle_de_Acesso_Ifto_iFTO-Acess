from django.urls import path, include
from gerenciar_controle_ifto.view import pessoa,rfid

urlpatterns = [
    path('cadastrar_rfid/', rfid.cadastrarRFID),
    path('editarRFID/', rfid.editarRFID),
]
