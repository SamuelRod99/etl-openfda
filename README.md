# Pipeline ETL de Dados de Eventos Adversos de Medicamentos

## Sobre o projeto

Este projeto consiste no desenvolvimento de um pipeline ETL (*Extract, Transform, Load*) em Python para coletar, organizar, transformar, validar e armazenar dados públicos sobre eventos adversos relacionados a medicamentos.

Os dados são obtidos por meio da API da [OpenFDA](https://open.fda.gov/apis/drug/event/), que disponibiliza informações sobre relatos de eventos adversos associados ao uso de medicamentos.

O objetivo é praticar conceitos fundamentais de Engenharia de Dados, desenvolvendo um processo automatizado e modular para transformar dados provenientes de uma API em arquivos estruturados, preparados para análises futuras e integração com bancos de dados.

## Objetivos

- Consumir uma API pública utilizando Python.
- Implementar a extração de dados com controle de quantidade de registros e paginação.
- Organizar os dados em estruturas reutilizáveis.
- Utilizar Pandas para criar e manipular DataFrames.
- Aplicar transformações e padronizações nos dados.
- Validar a estrutura e a quantidade dos dados extraídos e transformados.
- Implementar tratamento de erros e registros de execução (*logging*).
- Armazenar os resultados em arquivos CSV.
- Preparar a estrutura do projeto para futuras integrações com bancos de dados.

## Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **Requests:** consumo da API HTTP.
- **Pandas:** organização e transformação dos dados.
- **Logging:** registro de informações, avisos e erros durante a execução.
- **Pathlib:** gerenciamento de caminhos e criação de diretórios.
- **OpenFDA API:** fonte pública dos dados.

## Etapas do pipeline ETL

### 1. Extract — Extração

O pipeline realiza requisições à API da OpenFDA para obter registros de eventos adversos relacionados a medicamentos.

Essa etapa contempla recursos como:

- Requisições HTTP com a biblioteca `requests`.
- Definição de parâmetros para controlar a quantidade de registros.
- Controle de paginação.
- Configuração de timeout.
- Verificação de respostas HTTP com `raise_for_status()`.
- Tratamento de exceções.
- Registro das etapas da extração por meio de logs.

### 2. Transform — Transformação

Após a extração, os dados são organizados em listas de dicionários, separando as informações por categoria:

- **Reports:** informações gerais dos relatos.
- **Patients:** informações dos pacientes.
- **Reactions:** reações adversas relatadas.
- **Drugs:** informações dos medicamentos envolvidos.

Em seguida, as listas são convertidas em DataFrames utilizando Pandas.

As transformações podem incluir:

- Padronização de campos e códigos.
- Organização das colunas.
- Conversão de tipos de dados.
- Conversão de datas para o formato `datetime`.
- Preparação dos dados para armazenamento estruturado.

### 3. Validate — Validação

O projeto possui módulos dedicados à validação dos dados.

Essa etapa busca verificar se as funções retornam estruturas adequadas e se a quantidade de registros está de acordo com o esperado.

As validações podem incluir:

- Verificação da estrutura dos dados.
- Conferência da quantidade de registros.
- Identificação de respostas vazias.
- Verificação dos dados antes do carregamento.

### 4. Load — Carregamento

Após a transformação e a validação, os DataFrames são armazenados em arquivos CSV.

Os arquivos são gravados no diretório `dados/`, utilizando a biblioteca `pathlib` para gerenciar os caminhos e `pandas` para exportar os dados.

Arquivos gerados:

- `dados_report.csv`
- `dados_patient.csv`
- `dados_reaction.csv`
- `dados_drug.csv`

Os arquivos são salvos sem o índice do DataFrame e com codificação UTF-8.

## 🚀 Como executar o projeto

### Pré-requisitos

- Python 3.10 ou superior, recomendado.
- Git instalado.
- Conexão com a internet para acessar a API.

### 1. Clone o repositório

```bash
git clone URL_DO_SEU_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd projeto-etl
```

### 2. Crie um ambiente virtual

No Windows:

```bash
python -m venv venv
```

Ative o ambiente:

```bash
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install requests pandas
```

### 4. Execute o pipeline

```bash
python main.py
```

Após a execução, verifique se os arquivos CSV foram criados no diretório `dados/`.

**Importante:** os comandos de execução pressupõem que `main.py` seja o arquivo principal e que as dependências e os caminhos estejam configurados conforme a estrutura real do projeto.

## Resultados esperados

Ao executar o pipeline, espera-se obter arquivos CSV separados por categoria de informação, facilitando a consulta, a análise e a utilização posterior dos dados.

Essa separação também permite evoluir o projeto para uma estrutura relacional em um banco de dados, relacionando relatos, pacientes, reações e medicamentos conforme os identificadores disponíveis na fonte.


## Fonte dos dados

Os dados são obtidos da OpenFDA, iniciativa da Food and Drug Administration (FDA), agência reguladora dos Estados Unidos.

Documentação oficial da API: https://open.fda.gov/apis/drug/event/

## Sobre o projeto

Este projeto tem finalidade educacional e faz parte do meu aprendizado em Python e Engenharia de Dados, com foco na construção de pipelines ETL, consumo de APIs, tratamento de dados e preparação para integração com bancos de dados.
