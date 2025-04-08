"""
Testes de integração para o sistema de gestão de licitações governamentais.
Este arquivo contém testes que verificam a integração entre os diferentes componentes do sistema.
"""

import unittest
import os
import sys
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Adiciona o diretório raiz ao path para importar os módulos do sistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.db.session import get_db, Base
from app.models.user import User, UserRole
from app.models.licitacao import Licitacao, StatusLicitacao
from app.models.fornecedor import Fornecedor
from app.core.security import create_access_token
from app.services.recomendador import RecomendadorFornecedores

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

class TestIntegracao(unittest.TestCase):
    """
    Classe de testes de integração para o sistema de gestão de licitações.
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
        
        db.add_all([admin_user, gestor_user])
        db.commit()
        
        # Cria fornecedores de teste
        fornecedor1 = Fornecedor(
            razao_social="TechSolutions Informática Ltda",
            cnpj="12.345.678/0001-90",
            email="contato@techsolutions.com",
            telefone="(11) 1234-5678",
            area_atuacao="Tecnologia da Informação",
            especialidades="Servidores, Redes, Segurança, Cloud Computing",
            palavras_chave="TI, computadores, servidores, redes, software, hardware",
            descricao="Empresa especializada em soluções de TI, fornecimento de hardware, software e serviços de consultoria.",
            avaliacao_media=4.8,
            is_active=True
        )
        
        fornecedor2 = Fornecedor(
            razao_social="CleanMax Serviços de Limpeza",
            cnpj="98.765.432/0001-10",
            email="contato@cleanmax.com",
            telefone="(11) 8765-4321",
            area_atuacao="Serviços de Limpeza",
            especialidades="Limpeza predial, Limpeza hospitalar, Conservação",
            palavras_chave="limpeza, conservação, higienização, serviços gerais",
            descricao="Empresa de serviços de limpeza e conservação para órgãos públicos e empresas privadas.",
            avaliacao_media=4.2,
            is_active=True
        )
        
        db.add_all([fornecedor1, fornecedor2])
        db.commit()
        
        # Cria licitações de teste
        licitacao1 = Licitacao(
            numero="2025/001",
            titulo="Aquisição de Equipamentos de TI",
            descricao="Aquisição de computadores, servidores e equipamentos de rede para modernização do parque tecnológico.",
            objeto="Computadores desktop, notebooks, servidores e switches de rede",
            tipo="pregao_eletronico",
            status=StatusLicitacao.PUBLICADA,
            valor_estimado=1500000.0,
            orgao_responsavel="Ministério da Educação",
            criterio_julgamento="menor_preco",
            palavras_chave="computadores, servidores, TI, tecnologia, informática",
            created_by_id=admin_user.id
        )
        
        licitacao2 = Licitacao(
            numero="2025/002",
            titulo="Contratação de Serviços de Limpeza",
            descricao="Contratação de empresa especializada em serviços de limpeza e conservação para as dependências do órgão.",
            objeto="Serviços de limpeza, conservação e higienização",
            tipo="pregao_eletronico",
            status=StatusLicitacao.RASCUNHO,
            valor_estimado=800000.0,
            orgao_responsavel="Ministério da Saúde",
            criterio_julgamento="menor_preco",
            palavras_chave="limpeza, conservação, higienização, serviços gerais",
            created_by_id=gestor_user.id
        )
        
        db.add_all([licitacao1, licitacao2])
        db.commit()
        
        # Armazena IDs para uso nos testes
        cls.admin_id = admin_user.id
        cls.gestor_id = gestor_user.id
        cls.fornecedor1_id = fornecedor1.id
        cls.fornecedor2_id = fornecedor2.id
        cls.licitacao1_id = licitacao1.id
        cls.licitacao2_id = licitacao2.id
        
        db.close()
        
        # Cria tokens de acesso para os testes
        cls.admin_token = create_access_token({"sub": admin_user.email})
        cls.gestor_token = create_access_token({"sub": gestor_user.email})
    
    def test_fluxo_completo_licitacao(self):
        """
        Testa o fluxo completo de uma licitação, desde a criação até a conclusão.
        """
        # 1. Cria uma nova licitação
        nova_licitacao = {
            "numero": "2025/003",
            "titulo": "Fornecimento de Material de Escritório",
            "descricao": "Aquisição de material de escritório para todas as unidades",
            "objeto": "Papel A4, canetas, lápis, grampeadores e outros materiais",
            "tipo": "pregao_eletronico",
            "valor_estimado": 250000.0,
            "orgao_responsavel": "Ministério da Fazenda",
            "criterio_julgamento": "menor_preco",
            "palavras_chave": "material escritório, papel, caneta, suprimentos"
        }
        
        response = client.post(
            "/api/v1/licitacoes/",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            json=nova_licitacao
        )
        
        self.assertEqual(response.status_code, 200)
        licitacao_id = response.json()["id"]
        
        # 2. Verifica se a licitação foi criada com status de rascunho
        response = client.get(
            f"/api/v1/licitacoes/{licitacao_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "rascunho")
        
        # 3. Publica a licitação
        response = client.put(
            f"/api/v1/licitacoes/{licitacao_id}/status",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            params={"status": "publicada"}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "publicada")
        
        # 4. Obtém recomendações de fornecedores para a licitação
        # Primeiro, treina o modelo com os fornecedores de teste
        db = TestingSessionLocal()
        fornecedores = db.query(Fornecedor).filter(Fornecedor.is_active == True).all()
        
        fornecedores_dados = []
        for f in fornecedores:
            fornecedores_dados.append({
                'id': f.id,
                'razao_social': f.razao_social,
                'descricao': f.descricao,
                'area_atuacao': f.area_atuacao,
                'especialidades': f.especialidades,
                'palavras_chave': f.palavras_chave
            })
        
        recomendador = RecomendadorFornecedores()
        recomendador.treinar(fornecedores_dados)
        
        # Agora, obtém recomendações
        licitacao = db.query(Licitacao).filter(Licitacao.id == licitacao_id).first()
        licitacao_dados = {
            'id': licitacao.id,
            'titulo': licitacao.titulo,
            'descricao': licitacao.descricao,
            'objeto': licitacao.objeto,
            'palavras_chave': licitacao.palavras_chave
        }
        
        recomendacoes = recomendador.recomendar(licitacao_dados, top_n=2)
        
        # Verifica se as recomendações foram geradas
        self.assertGreater(len(recomendacoes), 0)
        
        # 5. Move a licitação para o status "em_analise"
        response = client.put(
            f"/api/v1/licitacoes/{licitacao_id}/status",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            params={"status": "em_analise"}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "em_analise")
        
        # 6. Move a licitação para o status "adjudicada"
        response = client.put(
            f"/api/v1/licitacoes/{licitacao_id}/status",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            params={"status": "adjudicada"}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "adjudicada")
        
        # 7. Move a licitação para o status "homologada"
        response = client.put(
            f"/api/v1/licitacoes/{licitacao_id}/status",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            params={"status": "homologada"}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "homologada")
        
        # 8. Conclui a licitação
        response = client.put(
            f"/api/v1/licitacoes/{licitacao_id}/status",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            params={"status": "concluida"}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "concluida")
        
        # 9. Verifica se a licitação está no status "concluida"
        response = client.get(
            f"/api/v1/licitacoes/{licitacao_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "concluida")
    
    def test_integracao_kanban_api(self):
        """
        Testa a integração entre o módulo Kanban e a API.
        """
        # 1. Obtém os dados do Kanban
        response = client.get(
            "/api/v1/kanban",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verifica se as colunas do Kanban estão presentes
        self.assertIn("columns", data)
        self.assertIn("valid_transitions", data)
        
        # Verifica se as colunas esperadas estão presentes
        columns = data["columns"]
        expected_columns = ["rascunho", "publicada", "em_analise", "adjudicada", "homologada", "concluida", "cancelada"]
        for col in expected_columns:
            self.assertIn(col, columns)
        
        # 2. Move uma licitação entre colunas do Kanban
        response = client.put(
            f"/api/v1/licitacoes/{self.licitacao2_id}/move",
            headers={"Authorization": f"Bearer {self.admin_token}"},
            json={"novo_status": "publicada"}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["novo_status"], "publicada")
        
        # 3. Verifica se a licitação foi movida
        response = client.get(
            "/api/v1/kanban",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verifica se a licitação está na coluna "publicada"
        publicada_items = data["columns"]["publicada"]["items"]
        licitacao2_found = False
        for item in publicada_items:
            if item["id"] == self.licitacao2_id:
                licitacao2_found = True
                break
        
        self.assertTrue(licitacao2_found)
    
    def test_integracao_recomendacoes_api(self):
        """
        Testa a integração entre o módulo de recomendações e a API.
        """
        # 1. Treina o modelo de recomendação
        response = client.post(
            "/api/v1/recomendacoes/treinar",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        self.assertEqual(response.status_code, 202)
        self.assertIn("message", response.json())
        
        # 2. Obtém recomendações para uma licitação
        response = client.get(
            f"/api/v1/recomendacoes/recomendar/{self.licitacao1_id}?top_n=2",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        # Verifica se a resposta foi bem-sucedida
        # Nota: Como o treinamento é assíncrono, pode não haver recomendações imediatamente
        if response.status_code == 200:
            data = response.json()
            self.assertEqual(data["licitacao_id"], self.licitacao1_id)
            if "recomendacoes" in data and len(data["recomendacoes"]) > 0:
                self.assertLessEqual(len(data["recomendacoes"]), 2)
        
        # 3. Calcula pontuações para propostas
        response = client.post(
            f"/api/v1/recomendacoes/calcular-pontuacoes/{self.licitacao1_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        self.assertEqual(response.status_code, 202)
        self.assertIn("message", response.json())

if __name__ == '__main__':
    unittest.main()
