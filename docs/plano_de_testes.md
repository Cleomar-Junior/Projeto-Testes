# Plano de Testes - Projeto Academia Gym

## 1. Objetivo
Este documento descreve a estratégia, o escopo e os procedimentos para os testes do projeto Academia Gym, visando garantir a qualidade, a funcionalidade e a segurança da aplicação.

## 2. Escopo
Os testes cobrirão os seguintes componentes:
- **Testes de Unidade:** Validação de modelos, serializers e views de forma isolada.
- **Testes de API:** Verificação dos endpoints REST para garantir que as requisições e respostas estão corretas.
- **Testes de Integração:** Validação da interação entre diferentes componentes (ex: criação de um usuário e sua mensalidade).
- **Testes de Mutação:** Análise da eficácia da suíte de testes existente.

## 3. Ferramentas
- **Framework de Testes:** Django Test Framework + DRF Test Client.
- **Cobertura de Código:** `coverage.py`.
- **Análise Estática:** SonarCloud (integrado via GitHub Actions).
- **Testes de Mutação:** `mutmut`.
- **Automação:** GitHub Actions.

## 4. Estrutura dos Testes
- Os testes estão localizados em `gym/tests.py`.
- Cada classe de teste corresponde a um modelo ou conjunto de funcionalidades (ex: `UsuarioCrudTest`, `MensalidadeCrudTest`).
- Os testes seguem o padrão "Arrange-Act-Assert".

## 5. Critérios de Sucesso
- Cobertura de código mínima de 70%.
- Zero Bugs críticos reportados pelo SonarCloud.
- Zero Vulnerabilidades de segurança.
- Atingir um alto percentual de mutações mortas com o `mutmut`.