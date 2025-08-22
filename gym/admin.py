from django.contrib import admin
from .models import Usuario, Mensalidade, Treino, Exercicio

admin.site.register(Usuario)
admin.site.register(Mensalidade)
admin.site.register(Treino)
admin.site.register(Exercicio)
