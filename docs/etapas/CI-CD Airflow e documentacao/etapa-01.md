# Etapa 01 — CI/CD com GitHub Actions

**Trilha:** CI-CD, Airflow e documentação (Edu)  
**Status:** concluída  
**Data:** 2026-09-07

## Objetivo

Automatizar as verificações mínimas do projeto e criar uma validação de build da imagem da API.

## Implementação

O workflow `.github/workflows/ci.yml` executa no `push` e no `pull_request` direcionados à branch `develop`:

1. instala o projeto e as dependências de desenvolvimento;
2. executa `flake8 src tests`;
3. executa `pytest -q`;
4. somente após as validações, executa `docker build --tag medical-text-triage:ci .`.

Assim, o repositório possui três automações verificáveis: lint, testes e build da imagem. O job de build depende do job `validate`, evitando publicar ou validar uma imagem quando o código já falhou nas checagens básicas.

## Reprodução local

Na raiz do repositório:

```powershell
python -m flake8 src tests
python -m pytest -q
docker build --tag medical-text-triage:local .
```

## Critério de aceite

- [x] Workflow versionado em `.github/workflows/ci.yml`.
- [x] Lint automatizado.
- [x] Testes automatizados.
- [x] Build Docker automatizado após lint e testes.