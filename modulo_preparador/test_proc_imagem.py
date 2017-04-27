from unittest import TestCase
from imagem import Imagem
import numpy

class TestPreprocessaImagem(TestCase):
	

	def test_carrega_imagem_unica(self):

		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')
		assert isinstance(im, Imagem)
		

	def test_encontra_contornos_imagem_unica(self):
		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')	
		contornos = im.encontra_contornos()
		assert isinstance(contornos, numpy.ndarray)

	def test_identificar_contornob_orda_externa_imagem_unica(self):
		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')	
		contornos = im.encontra_contornos()
		assert len(contornos) == 4

	def test_salvar_imagem_unica_processada_binaria(self):
		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')	
		result = im.salvar_imagem_processada("BI", "out_binarizada.jpg")
		assert isinstance(im, Imagem) 
		assert result == True

	def test_salvar_imagem_unica_processada_cinza(self):
		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')	
		result = im.salvar_imagem_processada("EC", "out_cinza.jpg")
		assert isinstance(im, Imagem) 
		assert result == True
	
	def test_salvar_imagem_unica_processada_colorida(self):
		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')	
		result = im.salvar_imagem_processada("CO", "out_colorida.jpg")
		assert isinstance(im, Imagem) 
		assert result == True


	def test_salvar_tipo_invalido_imagem(self):
		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')	
		result = im.salvar_imagem_processada("XX", "out_colorida.jpg")
		assert result == False

	def test_gera_texto_ocr_imagem_unica_colorida(self):
		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')	
		im.salvar_imagem_processada("CO", "out_colorida.jpg")
		im.gera_arquivo_texto('out_colorida.jpg', 'out_colorida.txt', 'por')
		arq = open('out_colorida.txt', 'r')
		assert arq.readlines()
		arq.close()

	def test_gera_texto_ocr_imagem_unica_cinza(self):
		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')	
		im.salvar_imagem_processada("EC", "out_cinza.jpg")
		im.gera_arquivo_texto('out_cinza.jpg','out_cinza.txt', 'por')
		arq = open('out_cinza.txt', 'r')
		assert arq.readlines()
		arq.close()

	def test_gera_texto_ocr_imagem_unica_binaria(self):
		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')	
		im.salvar_imagem_processada("BI", "out_binarizada.jpg")
		im.gera_arquivo_texto('out_binarizada.jpg', 'out_binarizada.txt', 'por')
		arq = open('out_binarizada.txt', 'r')
		assert arq.readlines()
		arq.close()

	def test_gera_pdf_imagem_unica_binaria(self):
		import os.path
		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')	
		im.salvar_imagem_processada("BI", "out_binarizada.jpg")
		im.gera_pdf("out_binarizada.jpg")
		assert os.path.exists("out_binarizada.pdf")

	def test_gera_pdf_imagem_unica_cinza(self):
		import os.path
		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')	
		im.salvar_imagem_processada("EC", "out_cinza.jpg")
		im.gera_pdf("out_cinza.jpg")
		assert os.path.exists("out_cinza.pdf")

	def test_gera_pdf_imagem_unica_colorida(self):
		import os.path
		im = Imagem('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1959_01__12_folha_de_ituiutaba/IMG_1642.JPG')	
		im.salvar_imagem_processada("CO", "out_colorida.jpg")
		im.gera_pdf("out_colorida.jpg")
		assert os.path.exists("out_colorida.pdf")

	def test_compacta_arquivo_pdf_colorido(self):
		import os.path
		im = Imagem()	
		im.compacta_pdf("out_colorida.pdf", "c_out_colorida.pdf")
		tamanho_input  =  os.path.getsize("out_colorida.pdf")
		tamanho_output =  os.path.getsize("c_out_colorida.pdf")
		assert tamanho_output < tamanho_input

	def test_insere_metadatos(self):
		#https://github.com/chrismattmann/tika-python (metadados de PDF em python)
		im = Imagem()
		im.insere_metadados("out_colorida.pdf", "1", im.transcricao_texto)



		
#https://guides.github.com/activities/hello-world/#pr
#http://bibdig.biblioteca.unesp.br/handle/10/27061
