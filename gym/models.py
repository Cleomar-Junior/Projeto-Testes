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
    is_personal = models.BooleanField(default=False)  # True = personal, False = aluno
    data_inscricao = models.DateField(auto_now_add=True)

    def __str__(self):
        tipo = "Personal" if self.is_personal else "Aluno"
        return f"{self.nome} ({tipo})"