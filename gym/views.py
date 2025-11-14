from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Usuario, Mensalidade, Treino, Exercicio
from django.db import models
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


# ============= TREINO CRUD =============
class TreinoListCreateView(generics.ListCreateAPIView):
    queryset = Treino.objects.select_related('aluno', 'personal').prefetch_related('exercicios')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TreinoCreateSerializer
        return TreinoSerializer
    
    def get_queryset(self):
        queryset = Treino.objects.select_related('aluno', 'personal').prefetch_related('exercicios')
        aluno_id = self.request.query_params.get('aluno')
        personal_id = self.request.query_params.get('personal')
        
        if aluno_id:
            queryset = queryset.filter(aluno_id=aluno_id)
        if personal_id:
            queryset = queryset.filter(personal_id=personal_id)
            
        return queryset


class TreinoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Treino.objects.select_related('aluno', 'personal').prefetch_related('exercicios')
    serializer_class = TreinoSerializer


# ============= EXERCÍCIO CRUD =============
class ExercicioListCreateView(generics.ListCreateAPIView):
    queryset = Exercicio.objects.select_related('treino')
    serializer_class = ExercicioSerializer
    
    def get_queryset(self):
        queryset = Exercicio.objects.select_related('treino')
        treino_id = self.request.query_params.get('treino')
        if treino_id:
            queryset = queryset.filter(treino_id=treino_id)
        return queryset


class ExercicioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercicio.objects.select_related('treino')
    serializer_class = ExercicioSerializer


# ============= VIEWS PERSONALIZADAS =============
@api_view(['GET'])
def alunos_personal(request, personal_id):
    """Lista todos os alunos que possuem treinos com um personal específico"""
    personal = get_object_or_404(Usuario, id=personal_id, is_personal=True)
    treinos = Treino.objects.filter(personal=personal).select_related('aluno')
    alunos = list(set([treino.aluno for treino in treinos]))
    serializer = UsuarioSerializer(alunos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def status_mensalidade(request, aluno_id):
    """Verifica o status da mensalidade de um aluno"""
    aluno = get_object_or_404(Usuario, id=aluno_id)
    from datetime import date
    
    try:
        ultima_mensalidade = Mensalidade.objects.filter(aluno=aluno).latest('validade')
        ativo = ultima_mensalidade.validade >= date.today()
        
        return Response({
            'aluno': aluno.nome,
            'ativo': ativo,
            'ultima_mensalidade': MensalidadeSerializer(ultima_mensalidade).data,
            'dias_restantes': (ultima_mensalidade.validade - date.today()).days if ativo else 0
        })
    except Mensalidade.DoesNotExist:
        return Response({
            'aluno': aluno.nome,
            'ativo': False,
            'ultima_mensalidade': None,
            'dias_restantes': 0
        })


@api_view(['GET'])
def dashboard_stats(request):
    """Estatísticas gerais da academia"""
    total_usuarios = Usuario.objects.count()
    total_alunos = Usuario.objects.filter(is_personal=False).count()
    total_personals = Usuario.objects.filter(is_personal=True).count()
    total_treinos = Treino.objects.count()
    
    # Alunos ativos (com mensalidade válida)
    from datetime import date
    mensalidades_ativas = Mensalidade.objects.filter(validade__gte=date.today())
    alunos_ativos = mensalidades_ativas.values_list('aluno', flat=True).distinct().count()
    
    return Response({
        'total_usuarios': total_usuarios,
        'total_alunos': total_alunos,
        'total_personals': total_personals,
        'total_treinos': total_treinos,
        'alunos_ativos': alunos_ativos,
        'alunos_inativos': total_alunos - alunos_ativos
    })

@api_view(['GET'])
def personal_mais_popular(request):
    """Retorna o personal trainer com o maior número de alunos distintos."""
    # Conta alunos distintos para cada personal e ordena de forma decrescente
    popular_personal = (
        Usuario.objects.filter(is_personal=True)
        .annotate(total_alunos=models.Count('treinos_orientados__aluno', distinct=True))
        .order_by('-total_alunos')
        .first()
    )

    if not popular_personal:
        return Response({"detail": "Nenhum personal trainer encontrado."}, status=404)

    serializer = UsuarioSerializer(popular_personal)
    return Response({
        **serializer.data,
        'total_alunos': popular_personal.total_alunos
    })