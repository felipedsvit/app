"""
Módulo de modelos de banco de dados para licitações do Sistema de Gestão de Licitações Governamentais.
Este módulo define o modelo de licitação com seus atributos e relacionamentos.
"""

from sqlalchemy import Column, String, DateTime, Enum, Text, ForeignKey, Float, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from ..db.session import Base

class StatusLicitacao(str, enum.Enum):
    """
    Enumeração para os status possíveis de uma licitação.
    Define as diferentes etapas do processo licitatório.
    """
    RASCUNHO = "rascunho"                 # Em elaboração
    PUBLICADA = "publicada"               # Publicada e aberta para propostas
    EM_ANALISE = "em_analise"             # Em análise de propostas
    ADJUDICADA = "adjudicada"             # Adjudicada a um fornecedor
    HOMOLOGADA = "homologada"             # Homologada pela autoridade competente
    CONCLUIDA = "concluida"               # Processo concluído
    CANCELADA = "cancelada"               # Processo cancelado
    SUSPENSA = "suspensa"                 # Processo temporariamente suspenso

class TipoLicitacao(str, enum.Enum):
    """
    Enumeração para os tipos de licitação conforme legislação brasileira.
    """
    CONCORRENCIA = "concorrencia"         # Concorrência
    TOMADA_PRECO = "tomada_preco"         # Tomada de Preços
    CONVITE = "convite"                   # Convite
    CONCURSO = "concurso"                 # Concurso
    LEILAO = "leilao"                     # Leilão
    PREGAO_ELETRONICO = "pregao_eletronico" # Pregão Eletrônico
    PREGAO_PRESENCIAL = "pregao_presencial" # Pregão Presencial
    DISPENSA = "dispensa"                 # Dispensa de Licitação
    INEXIGIBILIDADE = "inexigibilidade"   # Inexigibilidade de Licitação

class Licitacao(Base):
    """
    Modelo de licitação para o Sistema de Gestão de Licitações Governamentais.
    
    Attributes:
        id: Identificador único da licitação (UUID)
        numero: Número da licitação (único)
        titulo: Título descritivo da licitação
        descricao: Descrição detalhada do objeto da licitação
        tipo: Tipo de licitação conforme legislação
        status: Status atual da licitação
        valor_estimado: Valor estimado da licitação
        data_publicacao: Data de publicação da licitação
        data_abertura: Data de abertura das propostas
        data_encerramento: Data de encerramento do processo
        orgao_responsavel: Órgão responsável pela licitação
        criterio_julgamento: Critério de julgamento das propostas
        documentos_url: URL para documentos da licitação
        requisitos: Requisitos técnicos em formato JSON
        created_at: Data e hora de criação do registro
        updated_at: Data e hora da última atualização
        created_by_id: ID do usuário que criou a licitação
        created_by: Relação com o usuário que criou a licitação
        propostas: Relação com as propostas recebidas
    """
    __tablename__ = "licitacoes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    numero = Column(String, unique=True, index=True, nullable=False)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=False)
    tipo = Column(Enum(TipoLicitacao), nullable=False)
    status = Column(Enum(StatusLicitacao), default=StatusLicitacao.RASCUNHO, nullable=False)
    valor_estimado = Column(Float, nullable=True)
    data_publicacao = Column(DateTime, nullable=True)
    data_abertura = Column(DateTime, nullable=False)
    data_encerramento = Column(DateTime, nullable=True)
    orgao_responsavel = Column(String, nullable=False)
    criterio_julgamento = Column(String, nullable=False)
    documentos_url = Column(String, nullable=True)
    requisitos = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relações
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_by = relationship("User", backref="licitacoes_criadas")
    propostas = relationship("Proposta", back_populates="licitacao", cascade="all, delete-orphan")
    
    def __repr__(self):
        """Representação em string do objeto Licitacao."""
        return f"<Licitacao {self.numero}: {self.titulo}>"

class Proposta(Base):
    """
    Modelo de proposta para uma licitação.
    
    Attributes:
        id: Identificador único da proposta (UUID)
        licitacao_id: ID da licitação relacionada
        fornecedor_id: ID do fornecedor que enviou a proposta
        valor: Valor proposto
        prazo_entrega: Prazo de entrega em dias
        descricao_tecnica: Descrição técnica da proposta
        documentos_url: URL para documentos da proposta
        status: Status da proposta
        pontuacao_ia: Pontuação calculada pelo sistema de IA
        created_at: Data e hora de criação do registro
        updated_at: Data e hora da última atualização
    """
    __tablename__ = "propostas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    licitacao_id = Column(UUID(as_uuid=True), ForeignKey("licitacoes.id"), nullable=False)
    fornecedor_id = Column(UUID(as_uuid=True), ForeignKey("fornecedores.id"), nullable=False)
    valor = Column(Float, nullable=False)
    prazo_entrega = Column(Integer, nullable=False)  # Em dias
    descricao_tecnica = Column(Text, nullable=True)
    documentos_url = Column(String, nullable=True)
    status = Column(String, nullable=False, default="enviada")
    pontuacao_ia = Column(Float, nullable=True)
    is_vencedora = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relações
    licitacao = relationship("Licitacao", back_populates="propostas")
    fornecedor = relationship("Fornecedor", back_populates="propostas")
    
    def __repr__(self):
        """Representação em string do objeto Proposta."""
        return f"<Proposta {self.id}: Licitação {self.licitacao_id}, Fornecedor {self.fornecedor_id}>"
