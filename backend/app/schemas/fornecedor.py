"""
Módulo de modelos de banco de dados para fornecedores do Sistema de Gestão de Licitações Governamentais.
Este módulo define o modelo de fornecedor com seus atributos e relacionamentos.
"""

from sqlalchemy import Column, String, DateTime, Text, Boolean, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from ..db.session import Base

class Fornecedor(Base):
    """
    Modelo de fornecedor para o Sistema de Gestão de Licitações Governamentais.
    
    Attributes:
        id: Identificador único do fornecedor (UUID)
        razao_social: Razão social do fornecedor
        nome_fantasia: Nome fantasia do fornecedor
        cnpj: CNPJ do fornecedor (único)
        endereco: Endereço completo do fornecedor
        telefone: Telefone de contato
        email: Email de contato
        website: Site do fornecedor
        area_atuacao: Área principal de atuação
        descricao: Descrição detalhada do fornecedor
        certificacoes: Lista de certificações do fornecedor
        avaliacao_media: Avaliação média do fornecedor (0-5)
        tempo_mercado: Tempo de atuação no mercado (em anos)
        capacidade_entrega: Capacidade de entrega (em unidades/mês)
        historico_entregas: Histórico de entregas em formato JSON
        is_active: Indica se o fornecedor está ativo
        created_at: Data e hora de criação do registro
        updated_at: Data e hora da última atualização
        user_id: ID do usuário associado ao fornecedor
        user: Relação com o usuário associado
        propostas: Relação com as propostas enviadas
    """
    __tablename__ = "fornecedores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    razao_social = Column(String, nullable=False)
    nome_fantasia = Column(String, nullable=True)
    cnpj = Column(String, unique=True, index=True, nullable=False)
    endereco = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    website = Column(String, nullable=True)
    area_atuacao = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    certificacoes = Column(ARRAY(String), nullable=True)
    avaliacao_media = Column(Float, default=0.0, nullable=False)
    tempo_mercado = Column(Integer, nullable=True)  # Em anos
    capacidade_entrega = Column(Integer, nullable=True)  # Em unidades/mês
    historico_entregas = Column(JSONB, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relações
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    user = relationship("User", backref="fornecedor")
    propostas = relationship("Proposta", back_populates="fornecedor")
    
    # Campos para o sistema de recomendação de IA
    vetor_caracteristicas = Column(ARRAY(Float), nullable=True)  # Vetor de características para similaridade
    palavras_chave = Column(ARRAY(String), nullable=True)  # Palavras-chave extraídas da descrição
    score_confiabilidade = Column(Float, default=0.0, nullable=False)  # Score calculado pela IA
    
    def __repr__(self):
        """Representação em string do objeto Fornecedor."""
        return f"<Fornecedor {self.cnpj}: {self.razao_social}>"

class AvaliacaoFornecedor(Base):
    """
    Modelo para avaliações de fornecedores.
    
    Attributes:
        id: Identificador único da avaliação (UUID)
        fornecedor_id: ID do fornecedor avaliado
        licitacao_id: ID da licitação relacionada
        avaliador_id: ID do usuário que fez a avaliação
        pontuacao: Pontuação atribuída (0-5)
        comentario: Comentário sobre a avaliação
        criterios: Critérios específicos avaliados em formato JSON
        created_at: Data e hora de criação do registro
    """
    __tablename__ = "avaliacoes_fornecedores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    fornecedor_id = Column(UUID(as_uuid=True), ForeignKey("fornecedores.id"), nullable=False)
    licitacao_id = Column(UUID(as_uuid=True), ForeignKey("licitacoes.id"), nullable=True)
    avaliador_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    pontuacao = Column(Float, nullable=False)  # 0-5
    comentario = Column(Text, nullable=True)
    criterios = Column(JSONB, nullable=True)  # Critérios específicos em JSON
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relações
    fornecedor = relationship("Fornecedor", backref="avaliacoes")
    licitacao = relationship("Licitacao", backref="avaliacoes_fornecedores")
    avaliador = relationship("User", backref="avaliacoes_realizadas")
    
    def __repr__(self):
        """Representação em string do objeto AvaliacaoFornecedor."""
        return f"<AvaliacaoFornecedor {self.id}: Fornecedor {self.fornecedor_id}, Pontuação {self.pontuacao}>"
