"""
Testes unitários para o módulo de recomendação de fornecedores.
Este arquivo contém testes para verificar o funcionamento do algoritmo de recomendação.
"""

import unittest
import os
import sys
import numpy as np
from pathlib import Path

# Adiciona o diretório raiz ao path para importar os módulos do sistema
sys.path.append(str(Path(__file__).parent.parent))

from app.services.recomendador import RecomendadorFornecedores

class TestRecomendador(unittest.TestCase):
    """
    Classe de testes para o módulo de recomendação de fornecedores.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste antes de cada teste.
        """
        self.recomendador = RecomendadorFornecedores()
        
        # Dados de exemplo para fornecedores
        self.fornecedores_exemplo = [
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
            }
        ]
        
        # Licitações de exemplo para testes
        self.licitacoes_exemplo = [
            {
                'id': '1',
                'titulo': 'Aquisição de Equipamentos de TI',
                'descricao': 'Aquisição de computadores, servidores e equipamentos de rede para modernização do parque tecnológico.',
                'objeto': 'Computadores desktop, notebooks, servidores e switches de rede',
                'palavras_chave': 'computadores, servidores, TI, tecnologia, informática'
            },
            {
                'id': '2',
                'titulo': 'Contratação de Serviços de Limpeza',
                'descricao': 'Contratação de empresa especializada em serviços de limpeza e conservação para as dependências do órgão.',
                'objeto': 'Serviços de limpeza, conservação e higienização',
                'palavras_chave': 'limpeza, conservação, higienização, serviços gerais'
            }
        ]
    
    def test_preprocessar_texto(self):
        """
        Testa a função de pré-processamento de texto.
        """
        texto = "Teste de Pré-processamento 123! @#$%"
        resultado = self.recomendador.preprocessar_texto(texto)
        
        # Verifica se o texto foi convertido para minúsculas
        self.assertNotIn("T", resultado)
        self.assertNotIn("P", resultado)
        
        # Verifica se caracteres especiais foram removidos
        self.assertNotIn("!", resultado)
        self.assertNotIn("@", resultado)
        self.assertNotIn("#", resultado)
        self.assertNotIn("$", resultado)
        self.assertNotIn("%", resultado)
        
        # Verifica se números foram removidos
        self.assertNotIn("1", resultado)
        self.assertNotIn("2", resultado)
        self.assertNotIn("3", resultado)
        
        # Verifica se o resultado contém apenas palavras e espaços
        self.assertTrue(all(c.isalpha() or c.isspace() for c in resultado))
    
    def test_treinar_modelo(self):
        """
        Testa o treinamento do modelo de recomendação.
        """
        # Treina o modelo com os fornecedores de exemplo
        self.recomendador.treinar(self.fornecedores_exemplo)
        
        # Verifica se os dados de fornecedores foram armazenados
        self.assertEqual(len(self.recomendador.fornecedores_dados), len(self.fornecedores_exemplo))
        
        # Verifica se os vetores foram gerados
        self.assertIsNotNone(self.recomendador.fornecedores_vetores)
        
        # Verifica se o número de vetores corresponde ao número de fornecedores
        if hasattr(self.recomendador.fornecedores_vetores, 'shape'):
            # Para vetores do Sentence Transformer
            self.assertEqual(self.recomendador.fornecedores_vetores.shape[0], len(self.fornecedores_exemplo))
        else:
            # Para matriz esparsa do TF-IDF
            self.assertEqual(self.recomendador.fornecedores_vetores.shape[0], len(self.fornecedores_exemplo))
    
    def test_recomendar_fornecedores(self):
        """
        Testa a recomendação de fornecedores para uma licitação.
        """
        # Treina o modelo com os fornecedores de exemplo
        self.recomendador.treinar(self.fornecedores_exemplo)
        
        # Obtém recomendações para a primeira licitação de exemplo (TI)
        recomendacoes = self.recomendador.recomendar(self.licitacoes_exemplo[0], top_n=2)
        
        # Verifica se o número correto de recomendações foi retornado
        self.assertEqual(len(recomendacoes), 2)
        
        # Verifica se as recomendações têm o formato esperado
        self.assertIn('fornecedor', recomendacoes[0])
        self.assertIn('pontuacao', recomendacoes[0])
        self.assertIn('ranking', recomendacoes[0])
        
        # Verifica se o fornecedor de TI está na primeira posição
        self.assertEqual(recomendacoes[0]['fornecedor']['id'], '1')
        
        # Obtém recomendações para a segunda licitação de exemplo (Limpeza)
        recomendacoes = self.recomendador.recomendar(self.licitacoes_exemplo[1], top_n=2)
        
        # Verifica se o fornecedor de limpeza está na primeira posição
        self.assertEqual(recomendacoes[0]['fornecedor']['id'], '2')
    
    def test_salvar_e_carregar_modelo(self):
        """
        Testa o salvamento e carregamento do modelo.
        """
        # Treina o modelo com os fornecedores de exemplo
        self.recomendador.treinar(self.fornecedores_exemplo)
        
        # Salva o modelo em um arquivo temporário
        modelo_path = "modelo_teste_temp.joblib"
        self.recomendador.salvar_modelo(modelo_path)
        
        # Verifica se o arquivo foi criado
        self.assertTrue(os.path.exists(modelo_path))
        
        # Cria uma nova instância do recomendador
        novo_recomendador = RecomendadorFornecedores()
        
        # Carrega o modelo salvo
        novo_recomendador.carregar_modelo(modelo_path)
        
        # Verifica se os dados foram carregados corretamente
        self.assertEqual(len(novo_recomendador.fornecedores_dados), len(self.fornecedores_exemplo))
        
        # Limpa o arquivo temporário
        if os.path.exists(modelo_path):
            os.remove(modelo_path)

if __name__ == '__main__':
    unittest.main()
