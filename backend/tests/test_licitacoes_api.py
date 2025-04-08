"""
Testes unitários para os endpoints da API de licitações.
Este arquivo contém testes para verificar o funcionamento dos endpoints da API.
"""

import unittest
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import get_db, Base
from app.models.user import User, UserRole
from app.models.licitacao import Licitacao, StatusLicitacao
from app.core.security import create_access_token

# Cria um banco de dados em memória para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobrescreve a dependência get_db para usar o banco de dados de teste
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Cliente de teste
client = TestClient(app)

class TestLicitacoesAPI(unittest.TestCase):
    """
    Classe de testes para os endpoints da API de licitações.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Configura o ambiente de teste antes de todos os testes.
        """
        # Cria as tabelas no banco de dados de teste
        Base.metadata.create_all(bind=engine)
        
        # Cria uma sessão para adicionar dados de teste
        db = TestingSessionLocal()
        
        # Cria usuários de teste
        admin_user = User(
            email="admin@example.com",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
            nome="Admin Teste",
            role=UserRole.ADMIN,
            is_active=True
        )
        
        gestor_user = User(
            email="gestor@example.com",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
            nome="Gestor Teste",
            role=UserRole.GESTOR,
            is_active=True
        )
        
        fornecedor_user = User(
            email="fornecedor@example.com",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
            nome="Fornecedor Teste",
            role=UserRole.FORNECEDOR,
            is_active=True
        )
        
        db.add_all([admin_user, gestor_user, fornecedor_user])
        db.commit()
        
        # Cria licitações de teste
        licitacao1 = Licitacao(
            numero="2025/001",
            titulo="Aquisição de Equipamentos de TI",
            descricao="Aquisição de computadores e servidores",
            tipo="pregao_eletronico",
            status=StatusLicitacao.PUBLICADA,
            valor_estimado=1500000.0,
            orgao_responsavel="Ministério da Educação",
            criterio_julgamento="menor_preco",
            created_by_id=admin_user.id
        )
        
        licitacao2 = Licitacao(
            numero="2025/002",
            titulo="Contratação de Serviços de Limpeza",
            descricao="Serviços de limpeza e conservação",
            tipo="pregao_eletronico",
            status=StatusLicitacao.RASCUNHO,
            valor_estimado=800000.0,
            orgao_responsavel="Ministério da Saúde",
            criterio_julgamento="menor_preco",
            created_by_id=gestor_user.id
        )
        
        db.add_all([licitacao1, licitacao2])
        db.commit()
        
        # Armazena IDs para uso nos testes
        cls.admin_id = admin_user.id
        cls.gestor_id = gestor_user.id
        cls.fornecedor_id = fornecedor_user.id
        cls.licitacao1_id = licitacao1.id
        cls.licitacao2_id = licitacao2.id
        
        db.close()
        
        # Cria tokens de acesso para os testes
        cls.admin_token = create_access_token({"sub": admin_user.email})
        cls.gestor_token = create_access_token({"sub": gestor_user.email})
        cls.fornecedor_token = create_access_token({"sub": fornecedor_user.email})
    
    def test_read_licitacoes(self):
        """
        Testa a listagem de licitações.
        """
        # Teste com usuário admin
        response = client.get(
            "/api/v1/licitacoes/",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verifica se retornou as duas licitações
        data = response.json()
        self.assertEqual(len(data), 2)
        
        # Teste com filtro de status
        response = client.get(
            "/api/v1/licitacoes/?status=publicada",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verifica se retornou apenas a licitação publicada
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["status"], "publicada")
    
    def test_create_licitacao(self):
        """
        Testa a criação de uma nova licitação.
        """
        # Dados da nova licitação
        nova_licitacao = {
            "numero": "2025/003",
            "titulo": "Fornecimento de Material de Escritório",
            "descricao": "Aquisição de material de escritório",
            "tipo": "pregao_eletronico",
            "valor_estimado": 250000.0,
            "orgao_responsavel": "Ministério da Fazenda",
            "criterio_julgamento": "menor_preco"
        }
        
        # Teste com usuário gestor
        response = client.post(
            "/api/v1/licitacoes/",
            headers={"Authorization": f"Bearer {self.gestor_token}"},
            json=nova_licitacao
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verifica se os dados da licitação foram salvos corretamente
        data = response.json()
        self.assertEqual(data["numero"], nova_licitacao["numero"])
        self.assertEqual(data["titulo"], nova_licitacao["titulo"])
        self.assertEqual(data["status"], "rascunho")  # Status inicial deve ser rascunho
        
        # Teste com usuário fornecedor (não deve ter permissão)
        response = client.post(
            "/api/v1/licitacoes/",
            headers={"Authorization": f"Bearer {self.fornecedor_token}"},
            json=nova_licitacao
        )
        
        # Verifica se a resposta foi de acesso negado
        self.assertEqual(response.status_code, 403)
    
    def test_read_licitacao(self):
        """
        Testa a leitura de uma licitação específica.
        """
        # Teste com usuário admin
        response = client.get(
            f"/api/v1/licitacoes/{self.licitacao1_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verifica se os dados da licitação estão corretos
        data = response.json()
        self.assertEqual(data["numero"], "2025/001")
        self.assertEqual(data["titulo"], "Aquisição de Equipamentos de TI")
        self.assertEqual(data["status"], "publicada")
        
        # Teste com ID inexistente
        response = client.get(
            "/api/v1/licitacoes/999999",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        # Verifica se a resposta foi de não encontrado
        self.assertEqual(response.status_code, 404)
    
    def test_update_licitacao(self):
        """
        Testa a atualização de uma licitação.
        """
        # Dados para atualização
        dados_atualizacao = {
            "titulo": "Aquisição de Equipamentos de TI Atualizados",
            "valor_estimado": 1600000.0
        }
        
        # Teste com usuário admin
        response = client.put(
            f"/api/v1/licitacoes/{self.licitacao1_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            json=dados_atualizacao
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verifica se os dados foram atualizados corretamente
        data = response.json()
        self.assertEqual(data["titulo"], dados_atualizacao["titulo"])
        self.assertEqual(data["valor_estimado"], dados_atualizacao["valor_estimado"])
        
        # Teste com usuário fornecedor (não deve ter permissão)
        response = client.put(
            f"/api/v1/licitacoes/{self.licitacao1_id}",
            headers={"Authorization": f"Bearer {self.fornecedor_token}"},
            json=dados_atualizacao
        )
        
        # Verifica se a resposta foi de acesso negado
        self.assertEqual(response.status_code, 403)
    
    def test_update_licitacao_status(self):
        """
        Testa a atualização do status de uma licitação.
        """
        # Teste com usuário gestor
        response = client.put(
            f"/api/v1/licitacoes/{self.licitacao1_id}/status",
            headers={"Authorization": f"Bearer {self.gestor_token}"},
            params={"status": "em_analise"}
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verifica se o status foi atualizado corretamente
        data = response.json()
        self.assertEqual(data["status"], "em_analise")
        
        # Teste com transição inválida (de em_analise para rascunho)
        response = client.put(
            f"/api/v1/licitacoes/{self.licitacao1_id}/status",
            headers={"Authorization": f"Bearer {self.gestor_token}"},
            params={"status": "rascunho"}
        )
        
        # Verifica se a resposta foi de requisição inválida
        self.assertEqual(response.status_code, 400)
    
    def test_delete_licitacao(self):
        """
        Testa o cancelamento de uma licitação.
        """
        # Teste com usuário admin
        response = client.delete(
            f"/api/v1/licitacoes/{self.licitacao2_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verifica se a licitação foi cancelada (não excluída)
        data = response.json()
        self.assertEqual(data["status"], "cancelada")
        
        # Teste com usuário fornecedor (não deve ter permissão)
        response = client.delete(
            f"/api/v1/licitacoes/{self.licitacao1_id}",
            headers={"Authorization": f"Bearer {self.fornecedor_token}"}
        )
        
        # Verifica se a resposta foi de acesso negado
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()
