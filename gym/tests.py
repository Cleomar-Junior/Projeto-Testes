from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from datetime import date, timedelta
import json

from .models import Usuario, Mensalidade, Treino, Exercicio


class UsuarioModelTest(TestCase):
    """Testes para o modelo Usuario"""
    
    def setUp(self):
        self.usuario_aluno = Usuario.objects.create(
            nome="João Silva",
            data_nascimento=date(1995, 5, 15),
            sexo="M",
            is_personal=False
        )
        
        self.usuario_personal = Usuario.objects.create(
            nome="Maria Personal",
            data_nascimento=date(1988, 8, 20),
            sexo="F",
            is_personal=True
        )
    
    def test_criar_usuario_aluno(self):
        """Testa se o usuário aluno foi criado corretamente"""
        self.assertEqual(self.usuario_aluno.nome, "João Silva")
        self.assertEqual(self.usuario_aluno.sexo, "M")
        self.assertFalse(self.usuario_aluno.is_personal)
        self.assertEqual(str(self.usuario_aluno), "João Silva (Aluno)")
    
    def test_criar_usuario_personal(self):
        """Testa se o usuário personal foi criado corretamente"""
        self.assertEqual(self.usuario_personal.nome, "Maria Personal")
        self.assertEqual(self.usuario_personal.sexo, "F")
        self.assertTrue(self.usuario_personal.is_personal)
        self.assertEqual(str(self.usuario_personal), "Maria Personal (Personal)")
    
    def test_data_inscricao_automatica(self):
        """Testa se a data de inscrição é definida automaticamente"""
        self.assertEqual(self.usuario_aluno.data_inscricao, date.today())


class MensalidadeModelTest(TestCase):
    """Testes para o modelo Mensalidade"""
    
    def setUp(self):
        self.aluno = Usuario.objects.create(
            nome="Aluno Teste",
            data_nascimento=date(1990, 1, 1),
            sexo="M",
            is_personal=False
        )
        
        self.mensalidade = Mensalidade.objects.create(
            aluno=self.aluno,
            data_pagamento=date.today(),
            valor=150.00,
            validade=date.today() + timedelta(days=30)
        )
    
    def test_criar_mensalidade(self):
        """Testa se a mensalidade foi criada corretamente"""
        self.assertEqual(self.mensalidade.aluno, self.aluno)
        self.assertEqual(self.mensalidade.valor, 150.00)
        self.assertTrue("Aluno Teste" in str(self.mensalidade))
    
    def test_relacionamento_aluno(self):
        """Testa o relacionamento entre mensalidade e aluno"""
        self.assertEqual(self.aluno.mensalidades.count(), 1)
        self.assertEqual(self.aluno.mensalidades.first(), self.mensalidade)


class TreinoModelTest(TestCase):
    """Testes para o modelo Treino"""
    
    def setUp(self):
        self.aluno = Usuario.objects.create(
            nome="Aluno Teste",
            is_personal=False
        )
        
        self.personal = Usuario.objects.create(
            nome="Personal Teste",
            is_personal=True
        )
        
        self.treino = Treino.objects.create(
            aluno=self.aluno,
            personal=self.personal,
            nome="Treino A",
            descricao="Treino de peito e tríceps"
        )
    
    def test_criar_treino(self):
        """Testa se o treino foi criado corretamente"""
        self.assertEqual(self.treino.aluno, self.aluno)
        self.assertEqual(self.treino.personal, self.personal)
        self.assertEqual(self.treino.nome, "Treino A")
        self.assertTrue("Treino A" in str(self.treino))
    
    def test_relacionamentos_treino(self):
        """Testa os relacionamentos do treino"""
        self.assertEqual(self.aluno.treinos.count(), 1)
        self.assertEqual(self.personal.treinos_orientados.count(), 1)


class ExercicioModelTest(TestCase):
    """Testes para o modelo Exercicio"""
    
    def setUp(self):
        self.aluno = Usuario.objects.create(nome="Aluno", is_personal=False)
        self.treino = Treino.objects.create(
            aluno=self.aluno,
            nome="Treino Teste"
        )
        
        self.exercicio = Exercicio.objects.create(
            treino=self.treino,
            nome="Supino",
            series=4,
            repeticoes=12,
            carga_kg=60.0
        )
    
    def test_criar_exercicio(self):
        """Testa se o exercício foi criado corretamente"""
        self.assertEqual(self.exercicio.nome, "Supino")
        self.assertEqual(self.exercicio.series, 4)
        self.assertEqual(self.exercicio.repeticoes, 12)
        self.assertEqual(self.exercicio.carga_kg, 60.0)
        self.assertEqual(str(self.exercicio), "Supino (4x12)")


class UsuarioAPITest(APITestCase):
    """Testes para a API de Usuários"""
    
    def setUp(self):
        self.usuario_data = {
            'nome': 'Teste API',
            'data_nascimento': '1990-01-01',
            'sexo': 'M',
            'is_personal': False
        }
    
    def test_criar_usuario(self):
        """Testa criação de usuário via API"""
        url = reverse('usuario-list-create')
        response = self.client.post(url, self.usuario_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertEqual(Usuario.objects.get().nome, 'Teste API')
    
    def test_listar_usuarios(self):
        """Testa listagem de usuários via API"""
        Usuario.objects.create(**self.usuario_data)
        
        url = reverse('usuario-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_filtrar_por_personal(self):
        """Testa filtro de personal trainers"""
        Usuario.objects.create(**self.usuario_data)
        personal_data = self.usuario_data.copy()
        personal_data.update({'nome': 'Personal', 'is_personal': True})
        Usuario.objects.create(**personal_data)
        
        url = reverse('usuario-list-create')
        response = self.client.get(url, {'is_personal': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], 'Personal')
    
    def test_buscar_usuario_especifico(self):
        """Testa busca de usuário específico"""
        usuario = Usuario.objects.create(**self.usuario_data)
        
        url = reverse('usuario-detail', kwargs={'pk': usuario.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Teste API')
    
    def test_atualizar_usuario(self):
        """Testa atualização de usuário"""
        usuario = Usuario.objects.create(**self.usuario_data)
        
        url = reverse('usuario-detail', kwargs={'pk': usuario.pk})
        updated_data = {'nome': 'Nome Atualizado'}
        response = self.client.patch(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usuario.refresh_from_db()
        self.assertEqual(usuario.nome, 'Nome Atualizado')
    
    def test_deletar_usuario(self):
        """Testa deleção de usuário"""
        usuario = Usuario.objects.create(**self.usuario_data)
        
        url = reverse('usuario-detail', kwargs={'pk': usuario.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Usuario.objects.count(), 0)


class MensalidadeAPITest(APITestCase):
    """Testes para a API de Mensalidades"""
    
    def setUp(self):
        self.aluno = Usuario.objects.create(
            nome='Aluno Teste',
            is_personal=False
        )
        
        self.mensalidade_data = {
            'aluno': self.aluno.pk,
            'data_pagamento': str(date.today()),
            'valor': '150.00',
            'validade': str(date.today() + timedelta(days=30))
        }
    
    def test_criar_mensalidade(self):
        """Testa criação de mensalidade via API"""
        url = reverse('mensalidade-list-create')
        response = self.client.post(url, self.mensalidade_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mensalidade.objects.count(), 1)
    
    def test_validacao_validade_anterior(self):
        """Testa validação de validade anterior ao pagamento"""
        invalid_data = self.mensalidade_data.copy()
        invalid_data['validade'] = str(date.today() - timedelta(days=1))
        
        url = reverse('mensalidade-list-create')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_filtrar_mensalidades_por_aluno(self):
        """Testa filtro de mensalidades por aluno"""
        Mensalidade.objects.create(**{
            'aluno': self.aluno,
            'data_pagamento': date.today(),
            'valor': 150.00,
            'validade': date.today() + timedelta(days=30)
        })
        
        url = reverse('mensalidade-list-create')
        response = self.client.get(url, {'aluno': self.aluno.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TreinoAPITest(APITestCase):
    """Testes para a API de Treinos"""
    
    def setUp(self):
        self.aluno = Usuario.objects.create(nome='Aluno', is_personal=False)
        self.personal = Usuario.objects.create(nome='Personal', is_personal=True)
        
        self.treino_data = {
            'aluno': self.aluno.pk,
            'personal': self.personal.pk,
            'nome': 'Treino A',
            'descricao': 'Descrição do treino'
        }
    
    def test_criar_treino(self):
        """Testa criação de treino via API"""
        url = reverse('treino-list-create')
        response = self.client.post(url, self.treino_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Treino.objects.count(), 1)
    
    def test_validacao_personal_invalido(self):
        """Testa validação de personal inválido"""
        aluno_como_personal = Usuario.objects.create(nome='Não Personal', is_personal=False)
        invalid_data = self.treino_data.copy()
        invalid_data['personal'] = aluno_como_personal.pk
        
        url = reverse('treino-list-create')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ExercicioAPITest(APITestCase):
    """Testes para a API de Exercícios"""
    
    def setUp(self):
        self.aluno = Usuario.objects.create(nome='Aluno', is_personal=False)
        self.treino = Treino.objects.create(aluno=self.aluno, nome='Treino')
        
        self.exercicio_data = {
            'treino': self.treino.pk,
            'nome': 'Supino',
            'series': 4,
            'repeticoes': 12,
            'carga_kg': 60.0
        }
    
    def test_criar_exercicio(self):
        """Testa criação de exercício via API"""
        url = reverse('exercicio-list-create')
        response = self.client.post(url, self.exercicio_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercicio.objects.count(), 1)
    
    def test_filtrar_exercicios_por_treino(self):
        """Testa filtro de exercícios por treino"""
        Exercicio.objects.create(**{
            'treino': self.treino,
            'nome': 'Supino',
            'series': 4,
            'repeticoes': 12
        })
        
        url = reverse('exercicio-list-create')
        response = self.client.get(url, {'treino': self.treino.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ViewsEspeciaisTest(APITestCase):
    """Testes para views personalizadas"""
    
    def setUp(self):
        self.aluno = Usuario.objects.create(nome='Aluno', is_personal=False)
        self.personal = Usuario.objects.create(nome='Personal', is_personal=True)
        
        # Criar treino para relacionar aluno e personal
        self.treino = Treino.objects.create(
            aluno=self.aluno,
            personal=self.personal,
            nome='Treino A'
        )
        
        # Criar mensalidade válida
        self.mensalidade = Mensalidade.objects.create(
            aluno=self.aluno,
            data_pagamento=date.today(),
            valor=150.00,
            validade=date.today() + timedelta(days=15)
        )
    
    def test_alunos_do_personal(self):
        """Testa endpoint de alunos de um personal"""
        url = reverse('alunos-personal', kwargs={'personal_id': self.personal.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], 'Aluno')
    
    def test_status_mensalidade_ativo(self):
        """Testa status de mensalidade ativa"""
        url = reverse('status-mensalidade', kwargs={'aluno_id': self.aluno.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ativo'])
        self.assertEqual(response.data['aluno'], 'Aluno')
        self.assertEqual(response.data['dias_restantes'], 15)
    
    def test_status_mensalidade_inativo(self):
        """Testa status de aluno sem mensalidade"""
        aluno_sem_mensalidade = Usuario.objects.create(nome='Sem Mensalidade', is_personal=False)
        
        url = reverse('status-mensalidade', kwargs={'aluno_id': aluno_sem_mensalidade.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['ativo'])
        self.assertEqual(response.data['dias_restantes'], 0)
    
    def test_dashboard_stats(self):
        """Testa estatísticas do dashboard"""
        url = reverse('dashboard-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_usuarios'], 2)
        self.assertEqual(response.data['total_alunos'], 1)
        self.assertEqual(response.data['total_personals'], 1)
        self.assertEqual(response.data['alunos_ativos'], 1)


class IntegracaoCompletaTest(APITestCase):
    """Teste de integração completo simulando uso real"""
    
    def test_fluxo_completo_academia(self):
        """Testa um fluxo completo de uso da academia"""
        
        # 1. Criar personal trainer
        personal_data = {
            'nome': 'Carlos Personal',
            'data_nascimento': '1985-03-10',
            'sexo': 'M',
            'is_personal': True
        }
        response = self.client.post(reverse('usuario-list-create'), personal_data, format='json')
        personal_id = response.data['id']
        
        # 2. Criar aluno
        aluno_data = {
            'nome': 'Ana Aluna',
            'data_nascimento': '1992-07-20',
            'sexo': 'F',
            'is_personal': False
        }
        response = self.client.post(reverse('usuario-list-create'), aluno_data, format='json')
        aluno_id = response.data['id']
        
        # 3. Criar mensalidade
        mensalidade_data = {
            'aluno': aluno_id,
            'data_pagamento': str(date.today()),
            'valor': '200.00',
            'validade': str(date.today() + timedelta(days=30))
        }
        response = self.client.post(reverse('mensalidade-list-create'), mensalidade_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 4. Criar treino
        treino_data = {
            'aluno': aluno_id,
            'personal': personal_id,
            'nome': 'Treino Funcional',
            'descricao': 'Treino para iniciantes'
        }
        response = self.client.post(reverse('treino-list-create'), treino_data, format='json')
        treino_id = response.data['id']
        
        # 5. Adicionar exercícios
        exercicios = [
            {'treino': treino_id, 'nome': 'Agachamento', 'series': 3, 'repeticoes': 15},
            {'treino': treino_id, 'nome': 'Flexão', 'series': 3, 'repeticoes': 10}
        ]
        
        for exercicio in exercicios:
            response = self.client.post(reverse('exercicio-list-create'), exercicio, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 6. Verificar se tudo está funcionando
        # Buscar treino completo
        response = self.client.get(reverse('treino-detail', kwargs={'pk': treino_id}))
        self.assertEqual(len(response.data['exercicios']), 2)
        
        # Verificar status da mensalidade
        response = self.client.get(reverse('status-mensalidade', kwargs={'aluno_id': aluno_id}))
        self.assertTrue(response.data['ativo'])
        
        # Verificar dashboard
        response = self.client.get(reverse('dashboard-stats'))
        self.assertEqual(response.data['total_usuarios'], 2)
        self.assertEqual(response.data['alunos_ativos'], 1)