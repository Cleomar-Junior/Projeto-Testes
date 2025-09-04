from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Usuario

class UsuarioCrudTest(APITestCase):
    def setUp(self):
        self.url = reverse('usuario-list-create')
        self.data = {
            "nome": "João da Silva",
            "data_nascimento": "2000-05-10",
            "sexo": "M",
            "is_personal": False
        }

    def test_criar_usuario(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertEqual(Usuario.objects.get().nome, "João da Silva")

    def test_listar_usuarios(self):
        Usuario.objects.create(nome="Maria Souza", sexo="F")
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], "Maria Souza")
