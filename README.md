# README - Sistema de Gestão de Licitações Governamentais

## Sobre o Projeto

O Sistema de Gestão de Licitações Governamentais é uma plataforma completa para gerenciamento de processos licitatórios, desenvolvida para atender às necessidades específicas de órgãos governamentais. O sistema incorpora tecnologias avançadas de Inteligência Artificial para recomendação de fornecedores, painéis Kanban para visualização do fluxo de trabalho, e automação de processos para aumentar a eficiência e transparência.

## Principais Funcionalidades

- Gestão completa do ciclo de vida de licitações
- Recomendação inteligente de fornecedores baseada em IA
- Visualização do fluxo de licitações através de painéis Kanban
- Automação de tarefas repetitivas
- Controle de acesso baseado em funções (RBAC)
- Conformidade com a LGPD e segurança avançada

## Tecnologias Utilizadas

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- Celery
- Redis
- PostgreSQL
- Sentence Transformers
- scikit-learn

### Frontend
- React
- Material-UI
- React Router
- React Query
- Formik
- Yup
- React Beautiful DnD

### DevOps
- Docker
- Docker Compose
- GitHub Actions
- Prometheus
- Grafana

## Estrutura do Projeto

```
sistema-licitacoes/
├── backend/           # API e lógica de negócio
├── frontend/          # Interface de usuário
├── docs/              # Documentação
├── deployment/        # Arquivos de implantação
├── docker-compose.yml # Configuração Docker Compose
├── Dockerfile.backend # Dockerfile para o backend
├── Dockerfile.frontend # Dockerfile para o frontend
└── run_tests.sh       # Script para execução de testes
```

## Instalação e Execução

### Pré-requisitos
- Docker e Docker Compose
- Git

### Passos para Instalação

1. Clone o repositório:
```bash
git clone https://github.com/organizacao/sistema-licitacoes.git
cd sistema-licitacoes
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com as configurações apropriadas
```

3. Inicie os contêineres Docker:
```bash
docker-compose up -d
```

4. Acesse o sistema através do navegador:
```
http://localhost:8000
```

## Documentação

A documentação completa do sistema está disponível nos seguintes arquivos:

- **Manual do Usuário**: `docs/manual_usuario.md`
- **Documentação Técnica**: `docs/documentacao_tecnica.md`
- **API (Swagger)**: Disponível em `http://localhost:8000/docs` quando o sistema está em execução

## Testes

Para executar os testes do sistema:

```bash
./run_tests.sh
```

Este script executa todos os testes unitários e de integração do backend e frontend.

## Licença

Este projeto está licenciado sob a Licença Pública Geral GNU (GPL) - veja o arquivo LICENSE para detalhes.

## Contato

Para suporte técnico ou dúvidas sobre o sistema:
- Email: suporte@licitagov.gov.br
- Telefone: (XX) XXXX-XXXX
# app
