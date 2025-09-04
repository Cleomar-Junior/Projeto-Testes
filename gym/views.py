from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Usuario, Mensalidade, Treino, Exercicio
from .serializers import (
    UsuarioSerializer, 
    MensalidadeSerializer, 
    TreinoSerializer, 
    TreinoCreateSerializer,
    ExercicioSerializer
)