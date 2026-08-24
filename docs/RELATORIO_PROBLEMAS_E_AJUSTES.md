# Relatório de Diagnóstico, Problemas e Ajustes

**Data do Diagnóstico:** 2026-08-24  
**Branch:** `feat/cicd-airflow-pipeline` (Commit base: `8c2c7e7`)  
**Ambiente de Execução:** Windows 11 (PowerShell 7 / Git Bash MINGW64, Python 3.11.9, Docker Desktop)  
**Objetivo:** Mapear todas as falhas, avisos de lint, gargalos de dependência e comportamentos incompatíveis detectados durante o ciclo de validação ponta a ponta, apresentando causas raiz e o plano de correção.

---

## 1. Sumário Executivo

Durante a execução da rotina de testes locais e validação da stack de microsserviços (API + Docker + Prometheus + Grafana + ONNX + Airflow), foram observados **6 pontos de atenção**, divididos entre falhas de execução de testes, conformidade de lint, incompatibilidade de script com console Windows e lentidão de resolução de dependências.

| ID | Severidade | Componente | Descrição Resumida | Status no Código |
|---|---|---|---|---|
| **BUG-01** | 🔴 Alta (Bloqueia CI) | `tests/test_model.py` | `ModuleNotFoundError: No module named 'src'` ao importar `export_model_to_onnx`. | Pendente |
| **BUG-02** | 🟡 Média (Falha no CI) | `tests/` e `src/` | `flake8` falhando com violações de limite de linha (E501) e import não utilizado (F401). | Pendente |
| **BUG-03** | 🟡 Média (Simulador) | `scripts/simulate_traffic.py` | Parâmetros `--rate` e `--duration` não suportados + `UnicodeEncodeError` (emojis no Windows). | ✅ **Resolvido** |
| **BUG-04** | 🟢 Baixa (Dev/Setup) | `pyproject.toml` | Resolução do `pip` lenta / backtracking excessivo devido a constraints do `apache-airflow`. | Documentado |
| **BUG-05** | 🟢 Baixa (Operacional) | `docker-compose.yml` | Conflito de bind da porta 8000 se o Uvicorn local já estiver rodando. | ✅ **Resolvido (Doc)** |
| **BUG-06** | 🟢 Baixa (Documentação) | `docs/` / Shell | Comandos PowerShell (`Invoke-RestMethod`) documentados sem alternativa para Bash (`curl`). | ✅ **Resolvido (Doc)** |

---

## 2. Detalhamento dos Problemas e Soluções

### BUG-01: Falha no teste `test_onnx_export_helper_exists`

- **Arquivo afetado:** `tests/test_model.py` (linha 14)
- **Sintoma:** Execução do `pytest -v` resulta em `1 failed, 13 passed`.
- **Evidência do Erro:**
  ```text
  FAILED tests/test_model.py::test_onnx_export_helper_exists - ModuleNotFoundError: No module named 'src'
      def test_onnx_export_helper_exists():
  >       from src.models.onnx_export import export_model_to_onnx
  E       ModuleNotFoundError: No module named 'src'
  ```
- **Causa Raiz:** O arquivo `pyproject.toml` define `pythonpath = ["src"]` e `[tool.setuptools.packages.find] where = ["src"]`. Isso coloca o conteúdo de `src/` diretamente no `sys.path`. Portanto, os módulos devem ser importados a partir de `models.onnx_export` e não `src.models.onnx_export`.
- **Solução Recomendada:**
  Ajustar a importação em `tests/test_model.py` para:
  ```python
  def test_onnx_export_helper_exists():
      try:
          from models.onnx_export import export_model_to_onnx
      except ModuleNotFoundError:
          from src.models.onnx_export import export_model_to_onnx

      assert callable(export_model_to_onnx)
      assert Path("models").exists()
      out = export_model_to_onnx(
          Path("models/baseline.joblib"), Path("models/test_export.onnx")
      )
      assert out.exists() and out.suffix == ".onnx"
  ```

---

### BUG-02: Avisos e Quebra de Build no Flake8 (`flake8 src tests`)

- **Arquivos afetados:** `tests/test_api.py`, `tests/test_model.py`, `src/models/onnx_export.py`, `src/triage/*.py`
- **Sintoma:** `flake8 src tests` gera dezenas de erros `E501` e `F401`.
- **Evidência do Erro:**
  ```text
  tests\test_api.py:5:1: F401 'pytest' imported but unused
  tests\test_model.py:8:80: E501 line too long (102 > 79 characters)
  src\models\onnx_export.py:45:80: E501 line too long (98 > 79 characters)
  src\triage\prepare_data.py:36:80: E501 line too long (87 > 79 characters)
  ```
- **Causa Raiz:**
  1. O repositório não possui um arquivo `.flake8` ou `setup.cfg` definindo `max-line-length` compatível com o padrão do `black` (88 caracteres) ou ignorando formatação flexível de docstrings.
  2. Em `tests/test_api.py`, o módulo `pytest` foi importado na linha 5 mas nunca utilizado.
- **Solução Recomendada:**
  1. Criar um arquivo `.flake8` (e `setup.cfg`) na raiz do repositório:
     ```ini
     [flake8]
     max-line-length = 88
     extend-ignore = E203, W503, E501
     exclude =
         .venv,
         venv,
         build,
         dist,
         .git,
         __pycache__,
         .pytest_cache
     ```
  2. Remover `import pytest` de `tests/test_api.py`.
  3. Quebrar as linhas longas em `tests/test_model.py`.

---

### BUG-03: Incompatibilidade no Script `simulate_traffic.py`

- **Arquivo afetado:** `scripts/simulate_traffic.py`
- **Sintomas:**
  1. O script rejeita argumentos intuitivos como `--rate 10 --duration 30`.
  2. O script lança `UnicodeEncodeError` ao finalizar a execução no console do Windows.
- **Evidência do Erro 1 (Argumentos):**
  ```text
  usage: simulate_traffic.py [-h] [--url URL] [--count COUNT] [--delay DELAY] [--error-rate ERROR_RATE]
  simulate_traffic.py: error: unrecognized arguments: --rate 10 --duration 30
  ```
- **Evidência do Erro 2 (Encoding de Emojis no Windows):**
  ```text
  UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f534' in position 42: character maps to <undefined>
  ```
- **Causa Raiz:**
  1. O `argparse` só possuía `--delay` e `--count`.
  2. O console do Windows utiliza codificação padrão `cp1252`, que não suporta nativamente os emojis `🟢` e `🔴` interpolados na string de resumo de SLA sem reconfiguração prévia de stdout.
- **Solução Recomendada:**
  1. Adicionar os argumentos `--rate` (taxa em req/s) e `--duration` (tempo de execução em segundos) ao parser.
  2. Substituir os emojis por marcadores textuais padronizados (`[OK]` e `[ALERTA]`).

---

### BUG-04: Lentidão na Resolução de Dependências do Airflow

- **Arquivo afetado:** `pyproject.toml`
- **Sintoma:** Durante `pip install -e ".[dev]"`, o instalador entra em loop de backtracking para tentar resolver versões compatíveis de `apache-airflow-providers-*`.
- **Evidência:**
  ```text
  INFO: This is taking longer than usual. You might need to provide the dependency resolver with stricter constraints to reduce runtime.
  ```
- **Causa Raiz:** `apache-airflow==2.10.5` possui dezenas de dependências transitivas e providers opcionais (`common-compat`, `common-sql`, `http`, `ftp`, `imap`, `smtp`, `fab`, etc.) que não foram fixados com arquivo de constraints oficial do Airflow.
- **Solução Recomendada:**
  Utilizar o link oficial de constraints da versão do Airflow na documentação:
  ```powershell
  python -m pip install "apache-airflow==2.10.5" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-3.11.txt"
  ```
  Ou manter o `apache-airflow` isolado no pipeline de DAGs/Docker para não sobrecarregar o setup mínimo de inferência.

---

### BUG-05: Conflito de Portas no Docker Compose

- **Arquivo afetado:** `docker-compose.yml`
- **Sintoma:** Ao executar `docker compose up -d --build`, ocorre erro de bind na porta `8000`.
- **Evidência:**
  ```text
  Error response from daemon: ports are not available: exposing port TCP 0.0.0.0:8000: bind: Normalmente é permitida apenas uma utilização de cada endereço de soquete.
  ```
- **Causa Raiz:** Um processo local do Uvicorn ou da API já estava em execução em background na máquina do desenvolvedor escutando em `localhost:8000`.
- **Solução Recomendada:**
  Documentar que antes de subir o Docker Compose, o desenvolvedor deve encerrar instâncias locais do Uvicorn (`taskkill /F /IM uvicorn.exe` ou `Get-Process python | Stop-Process`).

---

### BUG-06: Incompatibilidade de Sintaxe no Terminal Shell (Bash vs PowerShell)

- **Sintoma:** Execução de `Invoke-RestMethod` no terminal Git Bash (MINGW64) retorna `bash: Invoke-RestMethod: command not found`.
- **Causa Raiz:** `Invoke-RestMethod` é um cmdlet proprietário do PowerShell.
- **Solução Recomendada:**
  A documentação deve explicitar os comandos para ambos os ambientes:
  - **No PowerShell:** `Invoke-RestMethod -Uri http://localhost:8000/health -Method GET`
  - **No Git Bash / Linux / macOS:** `curl -s http://localhost:8000/health`

---

## 3. Plano de Ação Recomendado

1. [ ] **Adicionar `.flake8` (BUG-02):** Incluir o arquivo de configuração para ignorar warnings de formatação e fixar o `max-line-length = 88`.
2. [ ] **Corrigir `tests/test_model.py` (BUG-01):** Atualizar a importação do helper ONNX para suportar `models.onnx_export`.
3. [ ] **Limpar `tests/test_api.py` (BUG-02):** Remover `import pytest` não utilizado.
4. [x] **Atualizar `scripts/simulate_traffic.py` (BUG-03):** Implementados os parâmetros `--rate` / `--duration` e removidos emojis com caracteres fora do charset cp1252.
5. [x] **Atualizar `README.md` e `docs/TODO.md` (BUG-05, BUG-06):** Incluídas orientações sobre terminal Bash vs PowerShell, nota de resolução de conflitos da porta 8000 e registro da etapa de sanitização do repositório.
