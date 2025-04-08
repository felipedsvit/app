"""
Documentação de usuário do Sistema de Gestão de Licitações Governamentais.
Este arquivo contém a documentação completa para usuários do sistema.
"""

# Manual do Usuário - Sistema de Gestão de Licitações Governamentais

## Sumário

1. [Introdução](#1-introdução)
2. [Requisitos do Sistema](#2-requisitos-do-sistema)
3. [Instalação e Configuração](#3-instalação-e-configuração)
4. [Acesso ao Sistema](#4-acesso-ao-sistema)
5. [Visão Geral da Interface](#5-visão-geral-da-interface)
6. [Módulos do Sistema](#6-módulos-do-sistema)
   - [6.1 Gestão de Licitações](#61-gestão-de-licitações)
   - [6.2 Gestão de Fornecedores](#62-gestão-de-fornecedores)
   - [6.3 Painel Kanban](#63-painel-kanban)
   - [6.4 Recomendações de Fornecedores](#64-recomendações-de-fornecedores)
   - [6.5 Gestão de Usuários](#65-gestão-de-usuários)
7. [Fluxos de Trabalho](#7-fluxos-de-trabalho)
8. [Perguntas Frequentes](#8-perguntas-frequentes)
9. [Suporte Técnico](#9-suporte-técnico)

## 1. Introdução

O Sistema de Gestão de Licitações Governamentais é uma plataforma completa para gerenciamento de processos licitatórios, desenvolvida para atender às necessidades específicas de órgãos governamentais. O sistema incorpora tecnologias avançadas de Inteligência Artificial para recomendação de fornecedores, painéis Kanban para visualização do fluxo de trabalho, e automação de processos para aumentar a eficiência e transparência.

### 1.1 Principais Funcionalidades

- Gestão completa do ciclo de vida de licitações
- Recomendação inteligente de fornecedores baseada em IA
- Visualização do fluxo de licitações através de painéis Kanban
- Automação de tarefas repetitivas
- Controle de acesso baseado em funções (RBAC)
- Conformidade com a LGPD e segurança avançada

### 1.2 Perfis de Usuário

O sistema suporta diferentes perfis de usuário, cada um com permissões específicas:

- **Administrador**: Acesso completo ao sistema, incluindo configurações, gestão de usuários e todas as funcionalidades.
- **Gestor**: Gerenciamento de licitações, aprovações e acesso às recomendações de IA.
- **Analista**: Análise de propostas, avaliação de fornecedores e visualização de recomendações.
- **Fornecedor**: Visualização de licitações públicas e envio de propostas.

## 2. Requisitos do Sistema

### 2.1 Requisitos de Hardware

- Processador: Intel Core i5 ou equivalente (ou superior)
- Memória RAM: 8GB (mínimo)
- Espaço em disco: 20GB disponíveis
- Conexão com a Internet: 10 Mbps (mínimo)

### 2.2 Requisitos de Software

- Sistema Operacional: Windows 10/11, macOS 10.15+, ou Linux (Ubuntu 20.04+)
- Navegador: Google Chrome 90+, Mozilla Firefox 88+, Microsoft Edge 90+, ou Safari 14+
- Docker e Docker Compose (para instalação local)

## 3. Instalação e Configuração

### 3.1 Instalação com Docker

1. Clone o repositório do sistema:
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

### 3.2 Configuração Inicial

Após a instalação, é necessário realizar a configuração inicial do sistema:

1. Acesse o sistema com as credenciais padrão:
   - Usuário: `admin@example.com`
   - Senha: `admin123`

2. Altere a senha padrão imediatamente após o primeiro acesso.

3. Configure os parâmetros básicos do sistema:
   - Informações da organização
   - Configurações de e-mail
   - Parâmetros de segurança

## 4. Acesso ao Sistema

### 4.1 Login

1. Acesse a URL do sistema através do navegador.
2. Na tela de login, insira seu e-mail e senha.
3. Clique no botão "Entrar".

### 4.2 Recuperação de Senha

1. Na tela de login, clique em "Esqueceu sua senha?".
2. Insira o e-mail associado à sua conta.
3. Siga as instruções enviadas para o seu e-mail para redefinir a senha.

### 4.3 Primeiro Acesso (Fornecedores)

1. Acesse a URL do sistema.
2. Clique em "Cadastre-se como Fornecedor".
3. Preencha o formulário com as informações solicitadas.
4. Aguarde a aprovação do administrador para acessar o sistema.

## 5. Visão Geral da Interface

### 5.1 Dashboard Principal

O Dashboard principal apresenta uma visão geral do sistema, com:

- Estatísticas de licitações (total, em andamento, concluídas)
- Gráficos de desempenho
- Licitações recentes
- Notificações e alertas
- Acesso rápido aos módulos principais

### 5.2 Menu de Navegação

O menu lateral permite acesso a todos os módulos do sistema:

- Dashboard
- Licitações
- Fornecedores
- Propostas
- Painel Kanban
- Recomendações
- Relatórios
- Configurações
- Usuários (apenas para administradores)

### 5.3 Barra Superior

A barra superior contém:

- Nome do usuário logado
- Perfil de acesso
- Notificações
- Opções de conta (perfil, configurações, sair)

## 6. Módulos do Sistema

### 6.1 Gestão de Licitações

#### 6.1.1 Listagem de Licitações

A tela de listagem de licitações apresenta todas as licitações do sistema, com opções de filtro por:

- Status (rascunho, publicada, em análise, adjudicada, homologada, concluída, cancelada)
- Tipo de licitação
- Período
- Órgão responsável
- Valor estimado

#### 6.1.2 Criação de Nova Licitação

Para criar uma nova licitação:

1. Clique no botão "Nova Licitação".
2. Preencha os campos obrigatórios:
   - Número da licitação
   - Título
   - Descrição
   - Objeto
   - Tipo de licitação
   - Valor estimado
   - Órgão responsável
   - Critério de julgamento
3. Adicione palavras-chave relevantes para melhorar as recomendações de IA.
4. Anexe documentos necessários.
5. Clique em "Salvar como Rascunho" ou "Publicar".

#### 6.1.3 Detalhes da Licitação

A tela de detalhes da licitação apresenta:

- Informações gerais da licitação
- Documentos anexados
- Histórico de alterações
- Propostas recebidas
- Fornecedores recomendados
- Opções de ação (editar, publicar, cancelar, etc.)

#### 6.1.4 Fluxo de Aprovação

O fluxo de aprovação de licitações segue as seguintes etapas:

1. **Rascunho**: Licitação em elaboração, visível apenas para criadores e administradores.
2. **Publicada**: Licitação publicada, visível para fornecedores.
3. **Em Análise**: Propostas sendo analisadas.
4. **Adjudicada**: Fornecedor selecionado.
5. **Homologada**: Licitação aprovada pela autoridade competente.
6. **Concluída**: Processo licitatório finalizado.
7. **Cancelada**: Licitação cancelada por algum motivo.

### 6.2 Gestão de Fornecedores

#### 6.2.1 Listagem de Fornecedores

A tela de listagem de fornecedores apresenta todos os fornecedores cadastrados, com opções de filtro por:

- Área de atuação
- Avaliação
- Status (ativo, inativo)
- Localização

#### 6.2.2 Cadastro de Fornecedor

Para cadastrar um novo fornecedor:

1. Clique no botão "Novo Fornecedor".
2. Preencha os campos obrigatórios:
   - Razão social
   - CNPJ
   - E-mail
   - Telefone
   - Área de atuação
   - Descrição
   - Especialidades
3. Adicione palavras-chave relevantes para melhorar as recomendações de IA.
4. Clique em "Salvar".

#### 6.2.3 Detalhes do Fornecedor

A tela de detalhes do fornecedor apresenta:

- Informações gerais do fornecedor
- Histórico de participação em licitações
- Avaliações recebidas
- Documentos anexados
- Opções de ação (editar, desativar, etc.)

#### 6.2.4 Avaliação de Fornecedores

Para avaliar um fornecedor:

1. Acesse a tela de detalhes do fornecedor.
2. Clique no botão "Avaliar Fornecedor".
3. Preencha o formulário de avaliação com notas para diferentes critérios.
4. Adicione comentários se necessário.
5. Clique em "Enviar Avaliação".

### 6.3 Painel Kanban

#### 6.3.1 Visão Geral do Kanban

O Painel Kanban apresenta as licitações organizadas por status, permitindo uma visualização clara do fluxo de trabalho. Cada coluna representa um status diferente:

- Rascunho
- Publicada
- Em Análise
- Adjudicada
- Homologada
- Concluída
- Cancelada

#### 6.3.2 Movimentação de Licitações

Para mover uma licitação entre os status:

1. Localize o card da licitação na coluna atual.
2. Arraste o card para a coluna de destino.
3. Confirme a ação na caixa de diálogo que aparecerá.

Observação: Apenas transições válidas são permitidas. Por exemplo, uma licitação em "Rascunho" só pode ser movida para "Publicada" ou "Cancelada".

#### 6.3.3 Filtros do Kanban

O Painel Kanban pode ser filtrado por:

- Órgão responsável
- Tipo de licitação
- Período
- Valor estimado
- Responsável

#### 6.3.4 Detalhes Rápidos

Para visualizar detalhes rápidos de uma licitação:

1. Clique no card da licitação no Kanban.
2. Um painel lateral será aberto com as informações principais.
3. Para acessar a tela completa de detalhes, clique em "Ver Detalhes".

### 6.4 Recomendações de Fornecedores

#### 6.4.1 Visão Geral das Recomendações

O módulo de Recomendações utiliza Inteligência Artificial para sugerir fornecedores adequados para cada licitação, com base em:

- Similaridade entre o objeto da licitação e a área de atuação do fornecedor
- Histórico de participação em licitações similares
- Avaliações recebidas
- Palavras-chave

#### 6.4.2 Acessando Recomendações

Para acessar as recomendações de fornecedores:

1. Acesse a tela de detalhes da licitação.
2. Clique na aba "Recomendações de Fornecedores".
3. Visualize a lista de fornecedores recomendados, ordenados por pontuação.

#### 6.4.3 Treinamento do Modelo de IA

Para treinar o modelo de IA (apenas para administradores e gestores):

1. Acesse o módulo de Recomendações.
2. Clique no botão "Treinar Modelo".
3. Aguarde a conclusão do treinamento.

Observação: O treinamento do modelo é realizado automaticamente quando novos fornecedores são cadastrados ou quando há alterações significativas nos dados.

#### 6.4.4 Convidando Fornecedores

Para convidar fornecedores recomendados:

1. Na lista de recomendações, localize o fornecedor desejado.
2. Clique no botão "Convidar" ao lado do fornecedor.
3. Confirme a ação na caixa de diálogo que aparecerá.
4. O fornecedor receberá um e-mail com o convite para participar da licitação.

### 6.5 Gestão de Usuários

#### 6.5.1 Listagem de Usuários

A tela de listagem de usuários (disponível apenas para administradores) apresenta todos os usuários do sistema, com opções de filtro por:

- Perfil de acesso
- Status (ativo, inativo)
- Órgão

#### 6.5.2 Criação de Novo Usuário

Para criar um novo usuário:

1. Clique no botão "Novo Usuário".
2. Preencha os campos obrigatórios:
   - Nome
   - E-mail
   - Perfil de acesso
   - Órgão
3. Clique em "Salvar".
4. O usuário receberá um e-mail com instruções para definir sua senha.

#### 6.5.3 Edição de Usuário

Para editar um usuário:

1. Localize o usuário na lista.
2. Clique no ícone de edição.
3. Altere as informações necessárias.
4. Clique em "Salvar".

#### 6.5.4 Desativação de Usuário

Para desativar um usuário:

1. Localize o usuário na lista.
2. Clique no ícone de desativação.
3. Confirme a ação na caixa de diálogo que aparecerá.

## 7. Fluxos de Trabalho

### 7.1 Fluxo Completo de Licitação

1. **Criação da Licitação**:
   - Usuário com perfil Gestor cria uma nova licitação.
   - Preenche todas as informações necessárias.
   - Salva como rascunho.

2. **Revisão e Publicação**:
   - Gestor revisa as informações da licitação.
   - Anexa documentos necessários.
   - Publica a licitação, alterando seu status para "Publicada".

3. **Recomendação de Fornecedores**:
   - Sistema gera automaticamente recomendações de fornecedores.
   - Gestor analisa as recomendações.
   - Opcionalmente, convida fornecedores recomendados.

4. **Recebimento de Propostas**:
   - Fornecedores visualizam a licitação publicada.
   - Enviam suas propostas dentro do prazo estabelecido.

5. **Análise de Propostas**:
   - Após o prazo, Gestor move a licitação para o status "Em Análise".
   - Sistema calcula pontuações para as propostas recebidas.
   - Analistas avaliam as propostas com base nos critérios definidos.

6. **Adjudicação**:
   - Gestor seleciona a proposta vencedora.
   - Move a licitação para o status "Adjudicada".
   - Sistema notifica o fornecedor selecionado.

7. **Homologação**:
   - Autoridade competente revisa o processo.
   - Gestor move a licitação para o status "Homologada".

8. **Conclusão**:
   - Após a execução do contrato, Gestor move a licitação para o status "Concluída".
   - Avalia o fornecedor com base no desempenho.

### 7.2 Fluxo de Cadastro de Fornecedor

1. **Solicitação de Cadastro**:
   - Fornecedor acessa o sistema.
   - Preenche o formulário de cadastro.
   - Envia a solicitação.

2. **Análise da Solicitação**:
   - Administrador ou Gestor recebe a solicitação.
   - Analisa as informações fornecidas.
   - Aprova ou rejeita o cadastro.

3. **Ativação da Conta**:
   - Se aprovado, fornecedor recebe e-mail de confirmação.
   - Define sua senha.
   - Acessa o sistema com suas credenciais.

4. **Complemento de Informações**:
   - Fornecedor complementa seu perfil com informações adicionais.
   - Anexa documentos necessários.

## 8. Perguntas Frequentes

### 8.1 Acesso ao Sistema

**P: Como recupero minha senha?**
R: Na tela de login, clique em "Esqueceu sua senha?" e siga as instruções enviadas para o seu e-mail.

**P: Por que não consigo acessar determinada funcionalidade?**
R: O acesso às funcionalidades depende do seu perfil de usuário. Consulte a seção 1.2 para mais informações sobre os perfis.

### 8.2 Licitações

**P: Por que não consigo mover uma licitação para determinado status?**
R: Apenas transições válidas são permitidas. Consulte a seção 6.3.2 para mais informações sobre as transições permitidas.

**P: Como anexo documentos a uma licitação?**
R: Na tela de detalhes da licitação, clique na aba "Documentos" e depois no botão "Anexar Documento".

### 8.3 Recomendações de IA

**P: Como o sistema gera recomendações de fornecedores?**
R: O sistema utiliza algoritmos de processamento de linguagem natural e similaridade de cosseno para comparar o objeto da licitação com as informações dos fornecedores.

**P: Por que as recomendações não estão aparecendo?**
R: Pode ser necessário treinar o modelo de IA. Consulte a seção 6.4.3 para mais informações.

## 9. Suporte Técnico

### 9.1 Canais de Atendimento

- **E-mail**: suporte@licitagov.gov.br
- **Telefone**: (XX) XXXX-XXXX
- **Chat**: Disponível no sistema, de segunda a sexta, das 8h às 18h

### 9.2 Reportando Problemas

Para reportar problemas:

1. Acesse o menu "Suporte".
2. Clique em "Reportar Problema".
3. Preencha o formulário com a descrição detalhada do problema.
4. Anexe capturas de tela se necessário.
5. Clique em "Enviar".

### 9.3 Atualizações do Sistema

O sistema é atualizado regularmente com novas funcionalidades e correções de bugs. As atualizações são anunciadas através de:

- Notificações no sistema
- E-mails para administradores
- Notas de versão disponíveis no menu "Sobre"
