#!/bin/bash

# Script para executar os testes do sistema de gestão de licitações governamentais
# Este script executa todos os testes unitários e de integração do backend e frontend

echo "=== Iniciando testes do Sistema de Gestão de Licitações Governamentais ==="
echo ""

# Diretório raiz do projeto
ROOT_DIR=$(pwd)
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

# Cores para saída
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para executar testes do backend
run_backend_tests() {
    echo -e "${YELLOW}Executando testes do backend...${NC}"
    cd "$BACKEND_DIR" || exit 1
    
    # Verifica se o ambiente virtual existe
    if [ ! -d "venv" ]; then
        echo "Criando ambiente virtual para testes..."
        python3 -m venv venv
    fi
    
    # Ativa o ambiente virtual
    source venv/bin/activate
    
    # Instala dependências de teste
    echo "Instalando dependências de teste..."
    pip install pytest pytest-cov httpx

    # Executa testes unitários
    echo -e "${YELLOW}Executando testes unitários do backend...${NC}"
    python -m pytest tests/test_recomendador.py -v
    UNIT_RESULT=$?
    
    # Executa testes de API
    echo -e "${YELLOW}Executando testes de API...${NC}"
    python -m pytest tests/test_licitacoes_api.py -v
    API_RESULT=$?
    
    # Executa testes de integração
    echo -e "${YELLOW}Executando testes de integração...${NC}"
    python -m pytest tests/test_integracao.py -v
    INTEGRATION_RESULT=$?
    
    # Desativa o ambiente virtual
    deactivate
    
    # Verifica resultados
    if [ $UNIT_RESULT -eq 0 ] && [ $API_RESULT -eq 0 ] && [ $INTEGRATION_RESULT -eq 0 ]; then
        echo -e "${GREEN}Todos os testes do backend passaram com sucesso!${NC}"
        return 0
    else
        echo -e "${RED}Alguns testes do backend falharam.${NC}"
        return 1
    fi
}

# Função para executar testes do frontend
run_frontend_tests() {
    echo -e "${YELLOW}Executando testes do frontend...${NC}"
    cd "$FRONTEND_DIR" || exit 1
    
    # Instala dependências de teste
    echo "Instalando dependências de teste..."
    npm install --no-save jest @testing-library/react @testing-library/jest-dom @testing-library/user-event jest-environment-jsdom babel-jest @babel/preset-env @babel/preset-react
    
    # Cria arquivo de configuração do Jest se não existir
    if [ ! -f "jest.config.js" ]; then
        echo "Criando configuração do Jest..."
        cat > jest.config.js << 'EOL'
module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': '<rootDir>/tests/__mocks__/styleMock.js',
    '\\.(jpg|jpeg|png|gif|webp|svg)$': '<rootDir>/tests/__mocks__/fileMock.js',
  },
  setupFilesAfterEnv: ['<rootDir>/tests/setupTests.js'],
};
EOL
    fi
    
    # Cria diretório de mocks se não existir
    mkdir -p tests/__mocks__
    
    # Cria mocks para arquivos estáticos
    echo "module.exports = {};" > tests/__mocks__/styleMock.js
    echo "module.exports = 'test-file-stub';" > tests/__mocks__/fileMock.js
    
    # Cria arquivo de setup para testes
    cat > tests/setupTests.js << 'EOL'
import '@testing-library/jest-dom';
EOL
    
    # Cria arquivo .babelrc se não existir
    if [ ! -f ".babelrc" ]; then
        echo "Criando configuração do Babel..."
        cat > .babelrc << 'EOL'
{
  "presets": ["@babel/preset-env", "@babel/preset-react"]
}
EOL
    fi
    
    # Executa testes
    echo -e "${YELLOW}Executando testes de componentes...${NC}"
    npx jest tests/Login.test.js tests/KanbanBoard.test.js tests/RecomendacoesFornecedores.test.js
    FRONTEND_RESULT=$?
    
    # Verifica resultados
    if [ $FRONTEND_RESULT -eq 0 ]; then
        echo -e "${GREEN}Todos os testes do frontend passaram com sucesso!${NC}"
        return 0
    else
        echo -e "${RED}Alguns testes do frontend falharam.${NC}"
        return 1
    fi
}

# Executa todos os testes
echo "=== Executando todos os testes ==="
echo ""

# Executa testes do backend
run_backend_tests
BACKEND_RESULT=$?

echo ""

# Executa testes do frontend
run_frontend_tests
FRONTEND_RESULT=$?

echo ""
echo "=== Resumo dos Resultados ==="

if [ $BACKEND_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ Testes do Backend: SUCESSO${NC}"
else
    echo -e "${RED}✗ Testes do Backend: FALHA${NC}"
fi

if [ $FRONTEND_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ Testes do Frontend: SUCESSO${NC}"
else
    echo -e "${RED}✗ Testes do Frontend: FALHA${NC}"
fi

echo ""

if [ $BACKEND_RESULT -eq 0 ] && [ $FRONTEND_RESULT -eq 0 ]; then
    echo -e "${GREEN}=== Todos os testes foram executados com sucesso! ===${NC}"
    exit 0
else
    echo -e "${RED}=== Alguns testes falharam. Verifique os logs para mais detalhes. ===${NC}"
    exit 1
fi
