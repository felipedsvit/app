"""
Documentação técnica do Sistema de Gestão de Licitações Governamentais.
Este arquivo contém a documentação técnica completa do sistema.
"""

# Documentação Técnica - Sistema de Gestão de Licitações Governamentais

## Sumário

1. [Visão Geral da Arquitetura](#1-visão-geral-da-arquitetura)
2. [Tecnologias Utilizadas](#2-tecnologias-utilizadas)
3. [Estrutura do Projeto](#3-estrutura-do-projeto)
4. [Backend](#4-backend)
5. [Frontend](#5-frontend)
6. [Módulo de IA](#6-módulo-de-ia)
7. [Banco de Dados](#7-banco-de-dados)
8. [Segurança](#8-segurança)
9. [Implantação](#9-implantação)
10. [Manutenção e Monitoramento](#10-manutenção-e-monitoramento)

## 1. Visão Geral da Arquitetura

O Sistema de Gestão de Licitações Governamentais é baseado em uma arquitetura moderna de microsserviços, com separação clara entre frontend e backend. A arquitetura foi projetada para ser escalável, segura e de fácil manutenção.

### 1.1 Diagrama de Arquitetura

```
+----------------------------------+
|           Cliente                |
|  (Navegador Web / Aplicativo)    |
+----------------------------------+
               |
               | HTTPS
               |
+----------------------------------+
|           Nginx                  |
|     (Proxy Reverso / SSL)        |
+----------------------------------+
               |
               |
  +------------+------------+
  |                         |
+--------------+    +---------------+
|   Frontend   |    |    Backend    |
|   (React)    |    |   (FastAPI)   |
+--------------+    +---------------+
                          |
                    +-----+------+
                    |            |
              +-----+----+  +----+-----+
              |PostgreSQL|  |  Redis   |
              |  (Dados) |  |  (Cache) |
              +----------+  +----------+
                    |
              +-----+-----+
              |  Celery   |
              | (Tarefas) |
              +-----------+
```

### 1.2 Fluxo de Dados

1. O cliente (navegador web) acessa o sistema através de HTTPS.
2. O Nginx atua como proxy reverso, direcionando as requisições para o frontend ou backend.
3. O frontend (React) renderiza a interface do usuário e se comunica com o backend via API REST.
4. O backend (FastAPI) processa as requisições, interage com o banco de dados e executa a lógica de negócio.
5. O PostgreSQL armazena todos os dados do sistema.
6. O Redis é utilizado para cache e como broker para o Celery.
7. O Celery executa tarefas assíncronas, como processamento de documentos e cálculos de IA.

## 2. Tecnologias Utilizadas

### 2.1 Backend

- **FastAPI**: Framework web de alta performance para APIs
- **SQLAlchemy**: ORM para interação com o banco de dados
- **Pydantic**: Validação de dados e configurações
- **Celery**: Processamento assíncrono de tarefas
- **Redis**: Cache e broker para Celery
- **JWT**: Autenticação baseada em tokens
- **Sentence Transformers**: Biblioteca para processamento de linguagem natural
- **scikit-learn**: Algoritmos de machine learning

### 2.2 Frontend

- **React**: Biblioteca JavaScript para construção de interfaces
- **Material-UI**: Componentes React com design Material
- **React Router**: Navegação entre páginas
- **React Query**: Gerenciamento de estado e cache
- **Formik**: Gerenciamento de formulários
- **Yup**: Validação de esquemas
- **React Beautiful DnD**: Funcionalidade de arrastar e soltar para o Kanban

### 2.3 Banco de Dados

- **PostgreSQL**: Banco de dados relacional
- **Alembic**: Migrações de banco de dados

### 2.4 DevOps

- **Docker**: Containerização
- **Docker Compose**: Orquestração de contêineres
- **GitHub Actions**: CI/CD
- **Prometheus**: Monitoramento
- **Grafana**: Visualização de métricas

## 3. Estrutura do Projeto

```
sistema-licitacoes/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── api_v1/
│   │   │       ├── endpoints/
│   │   │       └── api.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── docs.py
│   │   │   ├── ia_integration.py
│   │   │   └── kanban_integration.py
│   │   ├── db/
│   │   │   └── session.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── licitacao.py
│   │   │   └── fornecedor.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── licitacao.py
│   │   │   └── fornecedor.py
│   │   ├── services/
│   │   │   └── recomendador.py
│   │   ├── utils/
│   │   ├── worker/
│   │   │   ├── celery.py
│   │   │   └── tasks.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_recomendador.py
│   │   ├── test_licitacoes_api.py
│   │   └── test_integracao.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   └── layouts/
│   │   ├── context/
│   │   │   └── AuthContext.js
│   │   ├── hooks/
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Licitacoes.js
│   │   │   ├── KanbanBoard.js
│   │   │   └── RecomendacoesFornecedores.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── recomendacoesService.js
│   │   │   ├── kanbanService.js
│   │   │   └── integracaoService.js
│   │   └── utils/
│   ├── tests/
│   │   ├── Login.test.js
│   │   ├── KanbanBoard.test.js
│   │   └── RecomendacoesFornecedores.test.js
│   └── package.json
├── docs/
│   ├── manual_usuario.md
│   └── documentacao_tecnica.md
├── deployment/
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── run_tests.sh
```

## 4. Backend

### 4.1 Estrutura do Backend

O backend é organizado em módulos, seguindo os princípios de Clean Architecture:

- **api**: Endpoints da API REST
- **core**: Configurações e funcionalidades centrais
- **db**: Configuração do banco de dados
- **models**: Modelos de dados (SQLAlchemy)
- **schemas**: Esquemas de validação (Pydantic)
- **services**: Serviços de negócio
- **utils**: Utilitários
- **worker**: Tarefas assíncronas (Celery)

### 4.2 API REST

A API segue os princípios RESTful e utiliza o FastAPI para fornecer:

- Documentação automática (OpenAPI/Swagger)
- Validação de dados
- Serialização/deserialização
- Gerenciamento de dependências
- Tratamento de erros

#### 4.2.1 Principais Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | /api/v1/auth/login | Autenticação de usuários |
| GET | /api/v1/users/me | Obter dados do usuário atual |
| GET | /api/v1/licitacoes/ | Listar licitações |
| POST | /api/v1/licitacoes/ | Criar nova licitação |
| GET | /api/v1/licitacoes/{id} | Obter detalhes de uma licitação |
| PUT | /api/v1/licitacoes/{id} | Atualizar licitação |
| PUT | /api/v1/licitacoes/{id}/status | Atualizar status da licitação |
| GET | /api/v1/fornecedores/ | Listar fornecedores |
| GET | /api/v1/recomendacoes/recomendar/{licitacao_id} | Obter recomendações de fornecedores |
| POST | /api/v1/recomendacoes/treinar | Treinar modelo de IA |
| GET | /api/v1/kanban | Obter dados do Kanban |

### 4.3 Autenticação e Autorização

O sistema utiliza OAuth2 com JWT (JSON Web Tokens) para autenticação e RBAC (Role-Based Access Control) para autorização.

#### 4.3.1 Fluxo de Autenticação

1. O usuário envia credenciais (email/senha) para `/api/v1/auth/login`.
2. O backend valida as credenciais e gera um token JWT.
3. O cliente armazena o token e o inclui no cabeçalho `Authorization` de todas as requisições subsequentes.
4. O backend valida o token e identifica o usuário em cada requisição.

#### 4.3.2 Controle de Acesso

O sistema implementa RBAC com os seguintes perfis:

- **ADMIN**: Acesso completo
- **GESTOR**: Gerenciamento de licitações e aprovações
- **ANALISTA**: Análise de propostas
- **FORNECEDOR**: Visualização de licitações e envio de propostas

### 4.4 Tarefas Assíncronas

O Celery é utilizado para executar tarefas assíncronas, como:

- Busca automática de licitações governamentais
- Processamento OCR de documentos
- Treinamento do modelo de IA
- Cálculo de pontuações de fornecedores
- Limpeza de dados conforme LGPD
- Sistema de notificações

## 5. Frontend

### 5.1 Estrutura do Frontend

O frontend é organizado em componentes React, seguindo os princípios de componentização e separação de responsabilidades:

- **components**: Componentes reutilizáveis
- **context**: Contextos React (como AuthContext)
- **hooks**: Hooks personalizados
- **pages**: Páginas da aplicação
- **services**: Serviços para comunicação com a API
- **utils**: Utilitários

### 5.2 Gerenciamento de Estado

O frontend utiliza uma combinação de:

- **Context API**: Para estado global (autenticação, tema)
- **React Query**: Para estado de servidor e cache
- **useState/useReducer**: Para estado local de componentes

### 5.3 Roteamento

O React Router é utilizado para navegação entre páginas, com as seguintes rotas principais:

- `/login`: Página de login
- `/`: Dashboard principal
- `/licitacoes`: Listagem de licitações
- `/licitacoes/:id`: Detalhes de uma licitação
- `/fornecedores`: Listagem de fornecedores
- `/fornecedores/:id`: Detalhes de um fornecedor
- `/kanban`: Painel Kanban
- `/recomendacoes/:licitacaoId`: Recomendações para uma licitação

### 5.4 Componentes Principais

#### 5.4.1 Painel Kanban

O componente KanbanBoard implementa um quadro Kanban interativo para visualização e gerenciamento do fluxo de licitações. Utiliza o React Beautiful DnD para funcionalidade de arrastar e soltar.

#### 5.4.2 Recomendações de Fornecedores

O componente RecomendacoesFornecedores exibe recomendações de fornecedores geradas pelo módulo de IA, com pontuações e opções para convidar fornecedores.

## 6. Módulo de IA

### 6.1 Visão Geral

O módulo de IA utiliza técnicas de processamento de linguagem natural (NLP) e similaridade de cosseno para recomendar fornecedores adequados para cada licitação.

### 6.2 Algoritmo de Recomendação

O algoritmo de recomendação segue os seguintes passos:

1. **Pré-processamento de texto**:
   - Conversão para minúsculas
   - Remoção de caracteres especiais
   - Remoção de números
   - Remoção de stopwords

2. **Geração de embeddings**:
   - Utiliza Sentence Transformers para gerar embeddings de texto
   - Fallback para TF-IDF quando necessário

3. **Cálculo de similaridade**:
   - Calcula a similaridade de cosseno entre os embeddings da licitação e dos fornecedores
   - Ordena os fornecedores por pontuação de similaridade

4. **Pós-processamento**:
   - Aplica filtros adicionais (como localização, capacidade, etc.)
   - Formata os resultados com informações detalhadas dos fornecedores

### 6.3 Treinamento do Modelo

O modelo é treinado com dados de fornecedores, incluindo:

- Razão social
- Descrição
- Área de atuação
- Especialidades
- Palavras-chave

O treinamento pode ser realizado manualmente pelos administradores ou automaticamente quando novos fornecedores são cadastrados.

### 6.4 Integração com o Sistema

O módulo de IA é integrado ao sistema através de:

- Endpoints da API para obter recomendações e treinar o modelo
- Tarefas Celery para processamento em background
- Interface de usuário para visualização e interação com as recomendações

## 7. Banco de Dados

### 7.1 Modelo de Dados

O sistema utiliza um banco de dados relacional (PostgreSQL) com o seguinte modelo:

#### 7.1.1 Tabelas Principais

- **users**: Usuários do sistema
- **licitacoes**: Licitações governamentais
- **fornecedores**: Fornecedores cadastrados
- **propostas**: Propostas enviadas pelos fornecedores
- **documentos**: Documentos anexados às licitações e propostas
- **avaliacoes**: Avaliações de fornecedores

#### 7.1.2 Relacionamentos

- Um usuário pode criar várias licitações (1:N)
- Uma licitação pode receber várias propostas (1:N)
- Um fornecedor pode enviar várias propostas (1:N)
- Uma licitação pode ter vários documentos (1:N)
- Um fornecedor pode receber várias avaliações (1:N)

### 7.2 Migrações

O Alembic é utilizado para gerenciar migrações de banco de dados, permitindo:

- Versionamento do esquema
- Atualizações incrementais
- Rollback em caso de problemas

## 8. Segurança

### 8.1 Autenticação e Autorização

Conforme descrito na seção 4.3, o sistema utiliza OAuth2 com JWT para autenticação e RBAC para autorização.

### 8.2 Proteção de Dados

O sistema implementa as seguintes medidas de proteção de dados:

- **Criptografia em trânsito**: HTTPS para todas as comunicações
- **Criptografia em repouso**: Dados sensíveis criptografados no banco de dados
- **Criptografia PGP**: Para documentos sensíveis
- **Sanitização de entrada**: Validação e sanitização de todos os dados de entrada
- **Proteção contra ataques comuns**: XSS, CSRF, SQL Injection, etc.

### 8.3 Conformidade com LGPD

O sistema está em conformidade com a Lei Geral de Proteção de Dados (LGPD), implementando:

- Consentimento explícito para coleta de dados
- Finalidade específica para uso dos dados
- Minimização de dados coletados
- Direito de acesso, correção e exclusão de dados
- Políticas de retenção e exclusão de dados
- Registro de operações de tratamento de dados

## 9. Implantação

### 9.1 Requisitos de Infraestrutura

- **Servidor**: 4 vCPUs, 8GB RAM (mínimo)
- **Armazenamento**: 50GB SSD (mínimo)
- **Sistema Operacional**: Ubuntu 20.04 LTS ou superior
- **Docker**: 20.10 ou superior
- **Docker Compose**: 2.0 ou superior

### 9.2 Implantação com Docker

O sistema pode ser implantado facilmente usando Docker e Docker Compose:

```bash
# Clonar o repositório
git clone https://github.com/organizacao/sistema-licitacoes.git
cd sistema-licitacoes

# Configurar variáveis de ambiente
cp .env.example .env
# Editar o arquivo .env com as configurações apropriadas

# Construir e iniciar os contêineres
docker-compose up -d
```

### 9.3 CI/CD

O sistema utiliza GitHub Actions para CI/CD, com os seguintes pipelines:

- **Testes**: Executa testes unitários e de integração a cada push
- **Build**: Constrói as imagens Docker a cada push na branch principal
- **Deploy**: Implanta automaticamente em ambiente de homologação após build bem-sucedido
- **Release**: Implanta em produção após aprovação manual

## 10. Manutenção e Monitoramento

### 10.1 Logs

O sistema utiliza o padrão de logging estruturado, com os seguintes níveis:

- **ERROR**: Erros que requerem intervenção imediata
- **WARNING**: Situações problemáticas que não impedem o funcionamento
- **INFO**: Informações gerais sobre o funcionamento do sistema
- **DEBUG**: Informações detalhadas para depuração

### 10.2 Monitoramento

O sistema utiliza Prometheus e Grafana para monitoramento, coletando métricas como:

- **Desempenho**: Tempo de resposta, throughput, uso de recursos
- **Disponibilidade**: Uptime, healthchecks
- **Erros**: Taxa de erros, exceções
- **Negócio**: Número de licitações, propostas, fornecedores, etc.

### 10.3 Backup e Recuperação

O sistema implementa as seguintes estratégias de backup:

- **Backup diário**: Dump completo do banco de dados
- **Backup incremental**: A cada 6 horas
- **Retenção**: 30 dias para backups diários, 7 dias para incrementais
- **Teste de recuperação**: Realizado semanalmente

### 10.4 Atualizações

O processo de atualização do sistema segue as seguintes etapas:

1. Testes em ambiente de desenvolvimento
2. Implantação em ambiente de homologação
3. Testes de aceitação
4. Implantação em produção com janela de manutenção
5. Monitoramento pós-implantação
6. Rollback em caso de problemas
