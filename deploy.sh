#!/bin/bash
# Script de implantação para o Sistema de Gestão de Licitações Governamentais
# Este script configura o ambiente e implanta o sistema em produção

# Cores para saída
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para exibir mensagens
log() {
  echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
  echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERRO: $1${NC}"
  exit 1
}

warning() {
  echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] AVISO: $1${NC}"
}

# Verifica se o Docker está instalado
check_docker() {
  log "Verificando instalação do Docker..."
  if ! command -v docker &> /dev/null; then
    error "Docker não está instalado. Por favor, instale o Docker antes de continuar."
  fi
  
  if ! command -v docker-compose &> /dev/null; then
    error "Docker Compose não está instalado. Por favor, instale o Docker Compose antes de continuar."
  fi
  
  log "Docker e Docker Compose estão instalados."
}

# Verifica se o arquivo .env existe
check_env() {
  log "Verificando arquivo de variáveis de ambiente..."
  if [ ! -f .env ]; then
    warning "Arquivo .env não encontrado. Criando a partir do exemplo..."
    if [ ! -f .env.prod.example ]; then
      error "Arquivo .env.prod.example não encontrado. Não é possível criar o arquivo .env."
    fi
    cp .env.prod.example .env
    warning "Arquivo .env criado. Por favor, edite-o com as configurações corretas antes de continuar."
    exit 1
  fi
  log "Arquivo .env encontrado."
}

# Cria diretórios necessários
create_directories() {
  log "Criando diretórios necessários..."
  mkdir -p deployment/prometheus
  mkdir -p deployment/grafana/provisioning/datasources
  mkdir -p deployment/grafana/provisioning/dashboards
  log "Diretórios criados."
}

# Cria arquivo de configuração do Prometheus
create_prometheus_config() {
  log "Criando configuração do Prometheus..."
  cat > deployment/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'backend'
    metrics_path: /api/v1/metrics
    static_configs:
      - targets: ['backend:8000']
EOF
  log "Configuração do Prometheus criada."
}

# Cria configuração do Grafana
create_grafana_config() {
  log "Criando configuração do Grafana..."
  
  # Datasource
  cat > deployment/grafana/provisioning/datasources/datasource.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF

  # Dashboard
  cat > deployment/grafana/provisioning/dashboards/dashboard.yml << EOF
apiVersion: 1

providers:
  - name: 'Default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    options:
      path: /var/lib/grafana/dashboards
EOF
  
  log "Configuração do Grafana criada."
}

# Implanta o sistema
deploy_system() {
  log "Iniciando implantação do sistema..."
  
  # Parar containers existentes
  log "Parando containers existentes..."
  docker-compose -f docker-compose.prod.yml down
  
  # Construir e iniciar containers
  log "Construindo e iniciando containers..."
  docker-compose -f docker-compose.prod.yml up -d --build
  
  # Verificar status
  log "Verificando status dos containers..."
  docker-compose -f docker-compose.prod.yml ps
  
  log "Sistema implantado com sucesso!"
  log "Backend disponível em: http://localhost:8000/api/v1/docs"
  log "Frontend disponível em: http://localhost"
  log "Grafana disponível em: http://localhost:3000"
  log "Prometheus disponível em: http://localhost:9090"
  log "Flower (monitoramento Celery) disponível em: http://localhost:5555"
}

# Função principal
main() {
  log "Iniciando script de implantação do Sistema de Gestão de Licitações Governamentais..."
  
  check_docker
  check_env
  create_directories
  create_prometheus_config
  create_grafana_config
  deploy_system
  
  log "Implantação concluída com sucesso!"
}

# Executa a função principal
main
