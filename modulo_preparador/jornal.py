import time
import img2pdf
import os
from documento import Documento
from datetime import datetime
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

class Jornal(Documento):
    """
        Autor: Janderson de Almeida Coelho da Silva
        Data de Modificação: 05/07/2017

        Este módulo será responsável para a execução do processo de criação
        de documentos digitalizados com reconhecimento óptico de caracteres
        Aqui está a classe que fará toda a criação e processamento das imagens digitalizadas,
        compilação em arquivos PDF e reconhecimento óptico de caracteres.     

    """
    def __init__(self, dados_jornal=dict):

        """ 
		    Método construdor da classe. Instancia a imagem para ser preprocessada
		    Exemplo de uso:

		    >>> jornal = Jornal(dados_jornal)

            O parâmetro da classe recebe um dicionário.
		"""
        
        self._data_publicacao = dados_jornal['data_publicacao']
        self._titulo_jornal = dados_jornal['titulo_jornal']
        self._descricao_jornal = dados_jornal['descricao_jornal']
        self._cidade = dados_jornal['cidade']
        self._estado = dados_jornal['estado']
        self._nome_arquivo = self._formata_nome_arquivo()
        self._lista_imagens = dados_jornal['imagens']

    def _formata_nome_arquivo(self):

        """
            Método que formata o nome do arquivo conforme a data de publicação fornecida pelo usuário
            Exemplo de saída: 1960_01_01_titulo_jornal.pdf

        """
        
        try:
            # invertendo a data digitada pelo usuário para o formato 'ano_mes_dia'
            data_string = self._data_publicacao.replace('/', '_', 3)
            data_convertida = datetime.strptime(data_string, '%d_%m_%Y')
            data_reformatada_string = data_convertida.strftime('%Y_%m_%d')

            # transfomando o título do jornal para o nome do arquivo
            titulo_jornal = self._titulo_jornal.replace(' ', '_')
            titulo_jornal = titulo_jornal.lower()
            nome_arquivo_formatado = data_reformatada_string + '_' + titulo_jornal + '.pdf'
            return nome_arquivo_formatado

        except ValueError as e:
            raise e

    def _data_publicacao_valida(self):
        try:
            time.strptime(self._data_publicacao, '%m/%d/%Y')
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

    # data de publicação do jornal
    @property
    def data_publicacao(self):
        '''
            Retorna o valor da data publicação do jornal caso esta seja válida
        '''
        if (self._data_publicacao_valida() == True):
            return self._data_publicacao
        else:
            raise ValueError('A data de publicação do jornal está inválida!')

    def gera_arquivo_jornal(self, caminho_arquivo=str):
        '''
            Método que cria o arquivo PDF a partir das imagens listadas no atributo
            self._lista_imagens e salva dentro do caminho fornecido pelo parâmetro caminho_arquivo
            caso não exista a pasta primeiramente será criada e logo depois o PDF será salvo dentro dela
        '''
        os.makedirs(caminho_arquivo, exist_ok=True)
        os.chdir(caminho_arquivo)
        with open(self._nome_arquivo, "wb") as f:
            self._lista_imagens.sort()
            f.write(img2pdf.convert(self._lista_imagens))
            f.close()

    def gera_ocr(self, caminho_arquivo=str):
        '''
            Principal método: Depois de criar o arquivo PDF um comando chamado ocrmypdf
            com alguns parâmetros será chamado do sistema operacional para executar o Tesseract
            Mais inforações sobre como funciona o ocrmypdf em:
            http://ocrmypdf.readthedocs.io/en/latest/

        '''
        os.chdir(caminho_arquivo)
        cpu_count = os.cpu_count() - 1
        comando_ocr = "ocrmypdf -d -r -v --jobs %d --title '%s' -l por %s %s" % (
        cpu_count, self._titulo_jornal, self.nome_arquivo, self.nome_arquivo)
        return os.system(comando_ocr)
