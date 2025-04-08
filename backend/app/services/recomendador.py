"""
Módulo de IA para recomendações de fornecedores no Sistema de Gestão de Licitações Governamentais.
Este módulo implementa algoritmos de processamento de linguagem natural e similaridade de cosseno
para recomendar fornecedores adequados para cada licitação.
"""

import numpy as np
import pandas as pd
import re
import logging
from typing import List, Dict, Tuple, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import joblib
import os
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RecomendadorFornecedores:
    """
    Classe para recomendação de fornecedores baseada em processamento de linguagem natural
    e similaridade de cosseno.
    """
    
    def __init__(self, modelo_path: Optional[str] = None):
        """
        Inicializa o recomendador de fornecedores.
        
        Args:
            modelo_path: Caminho opcional para um modelo pré-treinado
        """
        self.modelo_path = modelo_path
        self.modelo = None
        self.vectorizer = TfidfVectorizer(
            min_df=2,
            max_df=0.85,
            ngram_range=(1, 2),
            stop_words=['de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'ao', 'ele', 'das', 'seu', 'sua', 'ou', 'quando', 'muito', 'nos', 'já', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'depois', 'sem', 'mesmo', 'aos', 'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'você', 'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha', 'numa', 'pelos', 'elas', 'qual', 'nós', 'lhe', 'deles', 'essas', 'esses', 'pelas', 'este', 'dele', 'tu', 'te', 'vocês', 'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas', 'dela', 'delas', 'esta', 'estes', 'estas', 'aquele', 'aquela', 'aqueles', 'aquelas', 'isto', 'aquilo', 'estou', 'está', 'estamos', 'estão', 'estive', 'esteve', 'estivemos', 'estiveram', 'estava', 'estávamos', 'estavam', 'estivera', 'estivéramos', 'esteja', 'estejamos', 'estejam', 'estivesse', 'estivéssemos', 'estivessem', 'estiver', 'estivermos', 'estiverem', 'hei', 'há', 'havemos', 'hão', 'houve', 'houvemos', 'houveram', 'houvera', 'houvéramos', 'haja', 'hajamos', 'hajam', 'houvesse', 'houvéssemos', 'houvessem', 'houver', 'houvermos', 'houverem', 'houverei', 'houverá', 'houveremos', 'houverão', 'houveria', 'houveríamos', 'houveriam', 'sou', 'somos', 'são', 'era', 'éramos', 'eram', 'fui', 'foi', 'fomos', 'foram', 'fora', 'fôramos', 'seja', 'sejamos', 'sejam', 'fosse', 'fôssemos', 'fossem', 'for', 'formos', 'forem', 'serei', 'será', 'seremos', 'serão', 'seria', 'seríamos', 'seriam', 'tenho', 'tem', 'temos', 'tém', 'tinha', 'tínhamos', 'tinham', 'tive', 'teve', 'tivemos', 'tiveram', 'tivera', 'tivéramos', 'tenha', 'tenhamos', 'tenham', 'tivesse', 'tivéssemos', 'tivessem', 'tiver', 'tivermos', 'tiverem', 'terei', 'terá', 'teremos', 'terão', 'teria', 'teríamos', 'teriam']
        )
        self.sentence_transformer = None
        self.fornecedores_vetores = None
        self.fornecedores_dados = None
        self.ultimo_treinamento = None
        
        # Carrega o modelo se o caminho for fornecido
        if modelo_path and os.path.exists(modelo_path):
            self.carregar_modelo(modelo_path)
        
    def preprocessar_texto(self, texto: str) -> str:
        """
        Pré-processa o texto para análise.
        
        Args:
            texto: Texto a ser pré-processado
            
        Returns:
            str: Texto pré-processado
        """
        if not texto:
            return ""
        
        # Converte para minúsculas
        texto = texto.lower()
        
        # Remove caracteres especiais e mantém apenas letras, números e espaços
        texto = re.sub(r'[^\w\s]', ' ', texto)
        
        # Remove números
        texto = re.sub(r'\d+', ' ', texto)
        
        # Remove espaços extras
        texto = re.sub(r'\s+', ' ', texto).strip()
        
        return texto
    
    def _inicializar_sentence_transformer(self):
        """
        Inicializa o modelo Sentence Transformer para embeddings de texto.
        """
        try:
            # Tenta carregar um modelo multilíngue para português
            self.sentence_transformer = SentenceTransformer('distiluse-base-multilingual-cased-v1')
            logger.info("Modelo Sentence Transformer carregado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao carregar o modelo Sentence Transformer: {str(e)}")
            # Fallback para TF-IDF se o modelo não puder ser carregado
            logger.info("Usando TF-IDF como fallback.")
            self.sentence_transformer = None
    
    def treinar(self, fornecedores: List[Dict[str, Any]]):
        """
        Treina o modelo com dados de fornecedores.
        
        Args:
            fornecedores: Lista de dicionários com dados de fornecedores
        """
        if not fornecedores:
            logger.warning("Nenhum fornecedor fornecido para treinamento.")
            return
        
        logger.info(f"Iniciando treinamento com {len(fornecedores)} fornecedores.")
        
        # Prepara os dados de texto para cada fornecedor
        textos = []
        for fornecedor in fornecedores:
            texto_combinado = " ".join([
                fornecedor.get('razao_social', ''),
                fornecedor.get('descricao', ''),
                fornecedor.get('area_atuacao', ''),
                fornecedor.get('especialidades', ''),
                fornecedor.get('palavras_chave', '')
            ])
            textos.append(self.preprocessar_texto(texto_combinado))
        
        # Inicializa o Sentence Transformer se ainda não foi inicializado
        if self.sentence_transformer is None:
            self._inicializar_sentence_transformer()
        
        # Gera embeddings usando Sentence Transformer se disponível
        if self.sentence_transformer:
            logger.info("Gerando embeddings com Sentence Transformer...")
            self.fornecedores_vetores = self.sentence_transformer.encode(textos)
        else:
            # Fallback para TF-IDF
            logger.info("Gerando embeddings com TF-IDF...")
            self.fornecedores_vetores = self.vectorizer.fit_transform(textos)
        
        # Armazena os dados dos fornecedores
        self.fornecedores_dados = fornecedores
        self.ultimo_treinamento = datetime.now()
        
        logger.info("Treinamento concluído com sucesso.")
    
    def recomendar(self, licitacao: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Recomenda fornecedores para uma licitação.
        
        Args:
            licitacao: Dicionário com dados da licitação
            top_n: Número de recomendações a retornar
            
        Returns:
            List[Dict[str, Any]]: Lista de fornecedores recomendados com pontuações
        """
        if self.fornecedores_vetores is None or self.fornecedores_dados is None:
            logger.error("Modelo não treinado. Execute o método treinar() primeiro.")
            return []
        
        logger.info(f"Gerando recomendações para licitação: {licitacao.get('titulo', 'Sem título')}")
        
        # Prepara o texto da licitação
        texto_licitacao = " ".join([
            licitacao.get('titulo', ''),
            licitacao.get('descricao', ''),
            licitacao.get('objeto', ''),
            licitacao.get('palavras_chave', '')
        ])
        texto_licitacao = self.preprocessar_texto(texto_licitacao)
        
        # Gera embedding para a licitação
        if self.sentence_transformer:
            vetor_licitacao = self.sentence_transformer.encode([texto_licitacao])[0].reshape(1, -1)
            # Calcula similaridade de cosseno
            similaridades = cosine_similarity(vetor_licitacao, self.fornecedores_vetores)[0]
        else:
            # Fallback para TF-IDF
            vetor_licitacao = self.vectorizer.transform([texto_licitacao])
            # Calcula similaridade de cosseno
            similaridades = cosine_similarity(vetor_licitacao, self.fornecedores_vetores)[0]
        
        # Obtém os índices dos fornecedores mais similares
        indices_top = similaridades.argsort()[-top_n:][::-1]
        
        # Prepara as recomendações
        recomendacoes = []
        for i, idx in enumerate(indices_top):
            if idx < len(self.fornecedores_dados):
                fornecedor = self.fornecedores_dados[idx]
                recomendacoes.append({
                    'fornecedor': fornecedor,
                    'pontuacao': float(similaridades[idx] * 100),  # Converte para porcentagem
                    'ranking': i + 1
                })
        
        logger.info(f"Geradas {len(recomendacoes)} recomendações.")
        return recomendacoes
    
    def salvar_modelo(self, caminho: str):
        """
        Salva o modelo treinado em disco.
        
        Args:
            caminho: Caminho para salvar o modelo
        """
        if self.fornecedores_vetores is None or self.fornecedores_dados is None:
            logger.error("Modelo não treinado. Execute o método treinar() primeiro.")
            return
        
        try:
            modelo_dados = {
                'fornecedores_vetores': self.fornecedores_vetores,
                'fornecedores_dados': self.fornecedores_dados,
                'vectorizer': self.vectorizer,
                'ultimo_treinamento': self.ultimo_treinamento
            }
            
            # Salva o modelo
            joblib.dump(modelo_dados, caminho)
            logger.info(f"Modelo salvo com sucesso em: {caminho}")
        except Exception as e:
            logger.error(f"Erro ao salvar o modelo: {str(e)}")
    
    def carregar_modelo(self, caminho: str):
        """
        Carrega um modelo treinado do disco.
        
        Args:
            caminho: Caminho do modelo a ser carregado
        """
        try:
            modelo_dados = joblib.load(caminho)
            
            self.fornecedores_vetores = modelo_dados['fornecedores_vetores']
            self.fornecedores_dados = modelo_dados['fornecedores_dados']
            self.vectorizer = modelo_dados['vectorizer']
            self.ultimo_treinamento = modelo_dados.get('ultimo_treinamento')
            
            logger.info(f"Modelo carregado com sucesso de: {caminho}")
            if self.ultimo_treinamento:
                logger.info(f"Data do último treinamento: {self.ultimo_treinamento}")
        except Exception as e:
            logger.error(f"Erro ao carregar o modelo: {str(e)}")
    
    def avaliar_recomendacoes(self, licitacoes_teste: List[Dict[str, Any]], fornecedores_corretos: List[List[str]]) -> Dict[str, float]:
        """
        Avalia a qualidade das recomendações usando métricas de precisão e recall.
        
        Args:
            licitacoes_teste: Lista de licitações para teste
            fornecedores_corretos: Lista de listas com IDs dos fornecedores corretos para cada licitação
            
        Returns:
            Dict[str, float]: Dicionário com métricas de avaliação
        """
        if len(licitacoes_teste) != len(fornecedores_corretos):
            logger.error("O número de licitações de teste deve ser igual ao número de listas de fornecedores corretos.")
            return {}
        
        precisao_total = 0.0
        recall_total = 0.0
        f1_total = 0.0
        
        for i, licitacao in enumerate(licitacoes_teste):
            recomendacoes = self.recomendar(licitacao, top_n=10)
            ids_recomendados = [r['fornecedor'].get('id') for r in recomendacoes]
            ids_corretos = fornecedores_corretos[i]
            
            # Calcula precisão (quantos dos recomendados são relevantes)
            relevantes_recomendados = set(ids_recomendados).intersection(set(ids_corretos))
            precisao = len(relevantes_recomendados) / len(ids_recomendados) if ids_recomendados else 0
            
            # Calcula recall (quantos dos relevantes foram recomendados)
            recall = len(relevantes_recomendados) / len(ids_corretos) if ids_corretos else 0
            
            # Calcula F1 (média harmônica entre precisão e recall)
            f1 = 2 * (precisao * recall) / (precisao + recall) if (precisao + recall) > 0 else 0
            
            precisao_total += precisao
            recall_total += recall
            f1_total += f1
        
        num_testes = len(licitacoes_teste)
        resultados = {
            'precisao_media': precisao_total / num_testes,
            'recall_medio': recall_total / num_testes,
            'f1_medio': f1_total / num_testes
        }
        
        logger.info(f"Avaliação concluída: {resultados}")
        return resultados


# Função para demonstração do uso do recomendador
def demonstracao_recomendador():
    """
    Função para demonstrar o uso do recomendador de fornecedores.
    """
    # Dados de exemplo para fornecedores
    fornecedores_exemplo = [
        {
            'id': '1',
            'razao_social': 'TechSolutions Informática Ltda',
            'descricao': 'Empresa especializada em soluções de TI, fornecimento de hardware, software e serviços de consultoria.',
            'area_atuacao': 'Tecnologia da Informação',
            'especialidades': 'Servidores, Redes, Segurança, Cloud Computing',
            'palavras_chave': 'TI, computadores, servidores, redes, software, hardware'
        },
        {
            'id': '2',
            'razao_social': 'CleanMax Serviços de Limpeza',
            'descricao': 'Empresa de serviços de limpeza e conservação para órgãos públicos e empresas privadas.',
            'area_atuacao': 'Serviços de Limpeza',
            'especialidades': 'Limpeza predial, Limpeza hospitalar, Conservação',
            'palavras_chave': 'limpeza, conservação, higienização, serviços gerais'
        },
        {
            'id': '3',
            'razao_social': 'PapelTudo Materiais de Escritório',
            'descricao': 'Distribuidora de materiais de escritório, papelaria e suprimentos para empresas e órgãos públicos.',
            'area_atuacao': 'Material de Escritório',
            'especialidades': 'Papelaria, Suprimentos de Informática, Mobiliário',
            'palavras_chave': 'papel, caneta, toner, impressora, material escritório'
        },
        {
            'id': '4',
            'razao_social': 'FrioCool Ar Condicionado e Refrigeração',
            'descricao': 'Empresa especializada em instalação e manutenção de sistemas de ar condicionado e refrigeração.',
            'area_atuacao': 'Refrigeração e Climatização',
            'especialidades': 'Ar condicionado, Refrigeração, Manutenção preventiva',
            'palavras_chave': 'ar condicionado, refrigeração, climatização, manutenção'
        },
        {
            'id': '5',
            'razao_social': 'SegurMax Serviços de Segurança',
            'descricao': 'Empresa de segurança patrimonial e pessoal, com serviços de vigilância e monitoramento.',
            'area_atuacao': 'Segurança',
            'especialidades': 'Vigilância, Monitoramento, Segurança eletrônica',
            'palavras_chave': 'segurança, vigilância, monitoramento, controle de acesso'
        },
        {
            'id': '6',
            'razao_social': 'DevPro Desenvolvimento de Software',
            'descricao': 'Empresa especializada em desenvolvimento de software, aplicativos e sistemas web.',
            'area_atuacao': 'Desenvolvimento de Software',
            'especialidades': 'Sistemas web, Aplicativos móveis, Inteligência artificial',
            'palavras_chave': 'so
(Content truncated due to size limit. Use line ranges to read in chunks)