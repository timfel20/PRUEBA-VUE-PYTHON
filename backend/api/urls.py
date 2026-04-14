from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('health/', views.health_check, name='health_check'),
]