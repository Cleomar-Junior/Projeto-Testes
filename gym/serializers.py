from rest_framework import serializers
from .models import Usuario, Mensalidade, Treino, Exercicio


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        
    def validate_data_nascimento(self, value):
        if value and value > serializers.DateField().to_representation(serializers.datetime.date.today()):
            raise serializers.ValidationError("Data de nascimento não pode ser futura.")
        return value


class MensalidadeSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    
    class Meta:
        model = Mensalidade
        fields = ['id', 'aluno', 'aluno_nome', 'data_pagamento', 'valor', 'validade']
    
    def validate(self, data):
        if data['validade'] < data['data_pagamento']:
            raise serializers.ValidationError("A validade não pode ser anterior à data de pagamento.")
        return data


class ExercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercicio
        fields = '__all__'


class TreinoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    personal_nome = serializers.CharField(source='personal.nome', read_only=True)
    exercicios = ExercicioSerializer(many=True, read_only=True)
    
    class Meta:
        model = Treino
        fields = ['id', 'aluno', 'aluno_nome', 'personal', 'personal_nome', 'nome', 'descricao', 'data_criacao', 'exercicios']


class TreinoCreateSerializer(serializers.ModelSerializer):
    """Serializer separado para criação de treinos sem exercícios aninhados"""
    class Meta:
        model = Treino
        fields = ['aluno', 'personal', 'nome', 'descricao']
        
    def validate_personal(self, value):
        if value and not value.is_personal:
            raise serializers.ValidationError("O usuário selecionado não é um personal trainer.")
        return value