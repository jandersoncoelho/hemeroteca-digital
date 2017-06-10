from documento import Documento
from datetime import datetime
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import time
import img2pdf

class Jornal(Documento):

	def __init__(self,dados_jornal=dict):

		self._data_publicacao 		= dados_jornal['data_publicacao']
		self._titulo_jornal       	= dados_jornal['titulo_jornal']
		self._descricao_jornal      = dados_jornal['descricao_jornal']
		self._cidade	   			= dados_jornal['cidade']
		self._estado				= dados_jornal['estado']
		self._nome_arquivo 			= self._formata_nome_arquivo()
		self._lista_imagens         = dados_jornal['imagens']
			
	def _formata_nome_arquivo(self):

		try:
			#invertendo a data digitada pelo usuário para o formato 'ano_mes_dia'
			data_string = self._data_publicacao.replace('/', '_',3)
			data_convertida =  datetime.strptime(data_string, '%d_%m_%Y')	
			data_reformatada_string = data_convertida.strftime('%Y_%m_%d')
		
			#transfomando o título do jornal para o nome do arquivo
			titulo_jornal = self._titulo_jornal.replace(' ','_')
			titulo_jornal = titulo_jornal.lower()
			nome_arquivo_formatado = data_reformatada_string + '_' + titulo_jornal + '.pdf'
			return nome_arquivo_formatado
		
		except ValueError as e:
			raise e
		

	def _data_publicacao_valida(self):
		try:
			data_valida = time.strptime(self._data_publicacao, '%m/%d/%Y')
			return True
		except ValueError:
			return False


	@property
	def dia(self):
		return self._dia 

	@property
	def mes(self):
		return self._mes

	@property
	def ano(self):
		return self._ano

	@property
	def cidade(self):
		return self._cidade

	@property
	def estado(self):
		
		return self._estado

	@property
	def descricao_jornal(self):		
		return self._descricao_jornal

	@property
	def nome_arquivo(self):
		return self._nome_arquivo 

	@property
	def titulo_jornal(self):
		return self._titulo_jornal

	#data de publicação do jornal
	@property
	def data_publicacao(self):
		#self._data_publicacao = ('%s/%s/%s' % (self._dia, self._mes, self._ano))
		if (self._data_publicacao_valida() == True):
			return self._data_publicacao
		else:
			raise ValueError('A data de publicação do jornal está inválida!')


	def gera_arquivo_jornal(self):

		with open(self._nome_arquivo,"wb") as f:
			self._lista_imagens.sort()
			f.write(img2pdf.convert(self._lista_imagens))
			f.close()

		