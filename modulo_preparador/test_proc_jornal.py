#from unittest import TestCase
import unittest
from jornal import Jornal

class TestProcessaJornal(unittest.TestCase):
	
	def test_cria_objeto_jornal(self):
		dados_jornal = { 
		                 'titulo_jornal':'Folha de Ituiutaba',
						 'data_publicacao':'10/10/1959',
						 'cidade':'Ituiutaba',
						 'estado':'MG',
						 'descricao_jornal':'',
						 'imagens':[]	
					   }
		jornal = Jornal(dados_jornal)
		assert isinstance(jornal, Jornal)
		del(jornal)

	def test_valida_dados_jornal(self):

		#testando se o usuário colocou a data certa
		dados_jornal = { 
		                 'titulo_jornal':'Folha de Ituiutaba',
						 'data_publicacao':'10/10/1959',
						 'cidade':'Ituiutaba',
						 'estado':'MG',
						 'descricao_jornal':'O jornal é teste!',	
						 'imagens':[]
					   }

		jornal = Jornal(dados_jornal)

		self.assertEqual(jornal.titulo_jornal, 'Folha de Ituiutaba')
		self.assertEqual(jornal.data_publicacao, '10/10/1959')
		self.assertEqual(jornal.cidade, 'Ituiutaba')
		self.assertEqual(jornal.estado, 'MG')
		self.assertEqual(jornal.descricao_jornal, 'O jornal é teste!')
		self.assertEqual(jornal.nome_arquivo, '1959_10_10_folha_de_ituiutaba.pdf')

		del(jornal)
		
		
	def test_valida_data_publicacao_jornal(self):
		#testando se o usuário colocou a data errada
		dados_jornal = { 
		                 'titulo_jornal':'Folha de Ituiutaba',
						 'data_publicacao':'31/02/1959',
						 'cidade':'Ituiutaba',
						 'estado':'MG',
						 'descricao_jornal':''	,
						 'imagens':[]

					   }
				
		with self.assertRaises(ValueError):
			jornal = Jornal(dados_jornal)
			print('valor de data incorrero')
			del(jornal)


	def test_gera_arquivo_pdf_jornal(self):

		lista_imagens = ['/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG',
						 '/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1643.JPG',
						 '/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1644.JPG',
						 '/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1645.JPG']
		dados_jornal = { 
		                 'titulo_jornal':'Folha de Ituiutaba',
						 'data_publicacao':'10/10/1959',
						 'cidade':'Ituiutaba',
						 'estado':'MG',
						 'descricao_jornal':'O jornal é teste!',
						 'imagens':lista_imagens	
					   }
		print (lista_imagens)

		jornal = Jornal(dados_jornal)
		jornal.gera_arquivo_jornal()

if __name__ == '__main__':
 	unittest.main()
	

	#hangout com Kent Back sobre TDD
	#https://www.youtube.com/watch?v=z9quxZsLcfo
		