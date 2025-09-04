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


# ============= USUÁRIO CRUD =============
class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def get_queryset(self):
        queryset = Usuario.objects.all()
        is_personal = self.request.query_params.get('is_personal')
        if is_personal is not None:
            queryset = queryset.filter(is_personal=is_personal.lower() == 'true')
        return queryset


class UsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


# ============= MENSALIDADE CRUD =============
class MensalidadeListCreateView(generics.ListCreateAPIView):
    queryset = Mensalidade.objects.select_related('aluno')
    serializer_class = MensalidadeSerializer
    
    def get_queryset(self):
        queryset = Mensalidade.objects.select_related('aluno')
        aluno_id = self.request.query_params.get('aluno')
        if aluno_id:
            queryset = queryset.filter(aluno_id=aluno_id)
        return queryset


class MensalidadeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mensalidade.objects.select_related('aluno')
    serializer_class = MensalidadeSerializer


