from django.urls import path
from . import views

urlpatterns = [
    # ============= USUÁRIOS =============
    path('usuarios/', views.UsuarioListCreateView.as_view(), name='usuario-list-create'),
    path('usuarios/<int:pk>/', views.UsuarioDetailView.as_view(), name='usuario-detail'),
    
    # ============= MENSALIDADES =============
    path('mensalidades/', views.MensalidadeListCreateView.as_view(), name='mensalidade-list-create'),
    path('mensalidades/<int:pk>/', views.MensalidadeDetailView.as_view(), name='mensalidade-detail'),
    
    # ============= TREINOS =============
    path('treinos/', views.TreinoListCreateView.as_view(), name='treino-list-create'),
    path('treinos/<int:pk>/', views.TreinoDetailView.as_view(), name='treino-detail'),
    
    # ============= EXERCÍCIOS =============
    path('exercicios/', views.ExercicioListCreateView.as_view(), name='exercicio-list-create'),
    path('exercicios/<int:pk>/', views.ExercicioDetailView.as_view(), name='exercicio-detail'),
    
    # ============= VIEWS PERSONALIZADAS =============
    path('personal/<int:personal_id>/alunos/', views.alunos_personal, name='alunos-personal'),
    path('aluno/<int:aluno_id>/status-mensalidade/', views.status_mensalidade, name='status-mensalidade'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
]