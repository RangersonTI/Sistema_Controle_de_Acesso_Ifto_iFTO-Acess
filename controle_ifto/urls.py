from django.urls import path
from . import view

urlpatterns = [
    path('prototipo_esp32/validarAcesso/',view.ValidarAcesso)
]
