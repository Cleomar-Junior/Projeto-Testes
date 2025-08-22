from django.db import models

# Create your models here.

class Usuario(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    is_personal = models.BooleanField(default=False)  # True = personal
    data_inscricao = models.DateField(auto_now_add=True)

    def __str__(self):
        tipo = "Personal" if self.is_personal else "Aluno"
        return f"{self.nome} ({tipo})"
    
class Mensalidade(models.Model):
    aluno = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="mensalidades")
    data_pagamento = models.DateField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    validade = models.DateField()  # Validade da mensalidade

    def __str__(self):
        return f"{self.aluno.nome} - Pago em {self.data_pagamento}"
    

class Treino(models.Model):
    aluno = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="treinos")
    personal = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="treinos_orientados")
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.aluno.nome})"