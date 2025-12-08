from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import date, timedelta
from .models import Usuario, Mensalidade, Treino, Exercicio

class UsuarioCrudTest(APITestCase):
    def setUp(self):
        self.url = reverse('usuario-list-create')
        self.personal_data = {
            "nome": "Carlos Personal",
            "is_personal": True
        }
        self.aluno_data = {
            "nome": "João Aluno",
            "data_nascimento": "2000-05-10",
            "sexo": "M",
            "is_personal": False
        }

    def test_criar_usuario(self):
        response = self.client.post(self.url, self.aluno_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertEqual(Usuario.objects.get().nome, "João Aluno")

    def test_listar_usuarios(self):
        Usuario.objects.create(**self.aluno_data)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], "João Aluno")

    def test_filtrar_usuarios_por_personal(self):
        Usuario.objects.create(**self.aluno_data)
        Usuario.objects.create(**self.personal_data)
        
        response = self.client.get(self.url, {'is_personal': 'true'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], "Carlos Personal")

    def test_detalhe_usuario(self):
        usuario = Usuario.objects.create(**self.aluno_data)
        url = reverse('usuario-detail', kwargs={'pk': usuario.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], "João Aluno")

    def test_atualizar_usuario(self):
        usuario = Usuario.objects.create(**self.aluno_data)
        url = reverse('usuario-detail', kwargs={'pk': usuario.pk})
        updated_data = {"nome": "João Silva", "is_personal": False}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usuario.refresh_from_db()
        self.assertEqual(usuario.nome, "João Silva")

    def test_deletar_usuario(self):
        usuario = Usuario.objects.create(**self.aluno_data)
        url = reverse('usuario-detail', kwargs={'pk': usuario.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Usuario.objects.count(), 0)

class MensalidadeCrudTest(APITestCase):
    def setUp(self):
        self.aluno = Usuario.objects.create(nome="Aluno Teste", is_personal=False)
        self.url = reverse('mensalidade-list-create')
        self.mensalidade_data = {
            "aluno": self.aluno.pk,
            "data_pagamento": date.today(),
            "valor": "150.00",
            "validade": date.today() + timedelta(days=30)
        }

    def test_criar_mensalidade(self):
        response = self.client.post(self.url, self.mensalidade_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mensalidade.objects.count(), 1)

    def test_filtrar_mensalidade_por_aluno(self):
        outro_aluno = Usuario.objects.create(nome="Outro Aluno", is_personal=False)
        Mensalidade.objects.create(aluno=outro_aluno, valor=100, data_pagamento=date.today(), validade=date.today()+timedelta(days=30))
        
        # ===== INÍCIO DA CORREÇÃO =====
        # Crie uma cópia dos dados para usar com o ORM
        orm_data = self.mensalidade_data.copy()
        # Substitua o ID (pk) pela instância do objeto
        orm_data['aluno'] = self.aluno 
        Mensalidade.objects.create(**orm_data)
        # ===== FIM DA CORREÇÃO =====
        
        response = self.client.get(self.url, {'aluno': self.aluno.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['aluno'], self.aluno.pk)

    def test_validacao_serializer_mensalidade(self):
        data_invalida = self.mensalidade_data.copy()
        data_invalida['validade'] = date.today() - timedelta(days=1) # Validade no passado
        response = self.client.post(self.url, data_invalida, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('A validade não pode ser anterior', str(response.data))

class CustomViewsTest(APITestCase):
    def setUp(self):
        self.personal = Usuario.objects.create(nome="Personal X", is_personal=True)
        self.aluno1 = Usuario.objects.create(nome="Aluno A", is_personal=False)
        self.aluno2 = Usuario.objects.create(nome="Aluno B", is_personal=False)
        
        # Criar treinos para associar alunos ao personal
        Treino.objects.create(aluno=self.aluno1, personal=self.personal, nome="Treino A")
        Treino.objects.create(aluno=self.aluno2, personal=self.personal, nome="Treino B")

    def test_alunos_personal_view(self):
        url = reverse('alunos-personal', kwargs={'personal_id': self.personal.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # Deve retornar aluno1 e aluno2
        nomes_alunos = [aluno['nome'] for aluno in response.data]
        self.assertIn("Aluno A", nomes_alunos)
        self.assertIn("Aluno B", nomes_alunos)

    def test_status_mensalidade_ativo(self):
        mensalidade_ativa = Mensalidade.objects.create(
            aluno=self.aluno1,
            data_pagamento=date.today(),
            validade=date.today() + timedelta(days=30),
            valor=100
        )
        url = reverse('status-mensalidade', kwargs={'aluno_id': self.aluno1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ativo'])
        self.assertGreaterEqual(response.data['dias_restantes'], 29)

    def test_status_mensalidade_inativo(self):
        # Aluno sem mensalidade
        url = reverse('status-mensalidade', kwargs={'aluno_id': self.aluno2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['ativo'])
        self.assertIsNone(response.data['ultima_mensalidade'])

    def test_dashboard_stats(self):
        # Criar dados para o dashboard
        Mensalidade.objects.create(aluno=self.aluno1, valor=100, data_pagamento=date.today(), validade=date.today()+timedelta(days=30))
        url = reverse('dashboard-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_usuarios'], 3)
        self.assertEqual(response.data['total_alunos'], 2)
        self.assertEqual(response.data['total_personals'], 1)
        self.assertEqual(response.data['alunos_ativos'], 1)
        self.assertEqual(response.data['alunos_inativos'], 1)

class TddExampleTest(APITestCase):
    def test_personal_mais_popular(self):
        # Setup: Cria personals e alunos
        personal1 = Usuario.objects.create(nome="Personal Ana", is_personal=True)
        personal2 = Usuario.objects.create(nome="Personal Bruno", is_personal=True)
        aluno1 = Usuario.objects.create(nome="Aluno 1", is_personal=False)
        aluno2 = Usuario.objects.create(nome="Aluno 2", is_personal=False)
        aluno3 = Usuario.objects.create(nome="Aluno 3", is_personal=False)

        # Associa alunos: Ana tem 2, Bruno tem 1
        Treino.objects.create(aluno=aluno1, personal=personal1, nome="Treino A")
        Treino.objects.create(aluno=aluno2, personal=personal1, nome="Treino B")
        Treino.objects.create(aluno=aluno3, personal=personal2, nome="Treino C")

        # Ação: Chama o novo endpoint
        url = reverse('personal-mais-popular') # URL ainda não existe
        response = self.client.get(url)

        # Asserção: Verifica o resultado esperado
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], "Personal Ana")
        self.assertEqual(response.data['total_alunos'], 2)

class CheckInViewTest(APITestCase):
    def setUp(self):
        # Cria um personal e um aluno
        self.personal = Usuario.objects.create(nome="Personal Zé", is_personal=True)
        self.aluno_ativo = Usuario.objects.create(nome="Aluno João", is_personal=False)
        self.aluno_inativo = Usuario.objects.create(nome="Aluno Maria", is_personal=False)
        
        # Cria uma mensalidade ativa para o aluno João
        Mensalidade.objects.create(
            aluno=self.aluno_ativo,
            data_pagamento=date.today(),
            validade=date.today() + timedelta(days=30),
            valor=100.0
        )
        # Cria uma mensalidade vencida para a aluna Maria
        Mensalidade.objects.create(
            aluno=self.aluno_inativo,
            data_pagamento=date.today() - timedelta(days=60),
            validade=date.today() - timedelta(days=30),
            valor=100.0
        )

    def test_checkin_sucesso_aluno_ativo(self):
        """Testa se um aluno com mensalidade ativa pode fazer check-in."""
        url = reverse('aluno-checkin', kwargs={'aluno_id': self.aluno_ativo.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Check-in realizado com sucesso", response.data['message'])
        self.assertEqual(CheckIn.objects.count(), 1)
        self.assertEqual(CheckIn.objects.first().aluno, self.aluno_ativo)

    def test_checkin_falha_aluno_inativo(self):
        """Testa se um aluno com mensalidade vencida NÃO pode fazer check-in."""
        url = reverse('aluno-checkin', kwargs={'aluno_id': self.aluno_inativo.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Mensalidade inativa", response.data['error'])
        self.assertEqual(CheckIn.objects.count(), 0)

    def test_checkin_falha_usuario_eh_personal(self):
        """Testa se um personal trainer NÃO pode fazer check-in."""
        url = reverse('aluno-checkin', kwargs={'aluno_id': self.personal.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Apenas alunos podem fazer check-in", response.data['error'])
        self.assertEqual(CheckIn.objects.count(), 0)