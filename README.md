# Projeto Academia Gym

Uma aplicação Django para gestão de academia, desenvolvida como parte da disciplina de Testes de Software.

## Sumário

- [Visão Geral](#-visão-geral)
- [Tecnologias](#️-tecnologias)
- [Documentação](#-documentação)
- [Começando](#-começando)
- [Testes e Qualidade](#-testes-e-qualidade)

## 📖 Visão Geral

Este projeto permite o gerenciamento de alunos, personals trainers, mensalidades, treinos e exercícios de uma academia, com uma API REST robusta e testada.

## Tecnologias

- **Backend:** Django, Django REST Framework
- **Banco de Dados:** SQLite (desenvolvimento)
- **Testes:** Django Test Framework, Coverage, Mutmut
- **CI/CD:** GitHub Actions, SonarCloud

## Documentação

- **[Manual de Execução](MANUAL.md)**: Guia passo a passo para rodar o projeto.
- **[Plano de Testes](docs/plano_de_testes.md)**: Estratégia e escopo dos testes da aplicação.
- **[Testes de Mutação](docs/testes_de_mutacao.md)**: Relatório e procedimentos dos testes de mutação.
- **[Relatório de Testes e Qualidade](README_TESTES.md)**: Documento detalhado sobre as atividades de teste realizadas.

## Começando

Para uma configuração rápida, siga o **[Manual de Execução](MANUAL.md)**.

## Testes e Qualidade

O projeto possui uma pipeline de CI/CD configurada para garantir a qualidade do código:

- **Cobertura de Testes:** Acima de 80%.
- **Análise Estática:** Integrada com SonarCloud.
- **Automação:** Testes e análise rodam a cada `push` via GitHub Actions.
