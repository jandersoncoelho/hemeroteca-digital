#from unittest import TestCase
import unittest
import glob
from jornal import Jornal
import os


class TestProcessaJornal(unittest.TestCase):

    def test_cria_objeto_jornal(self):
        dados_jornal = {
            'titulo_jornal': 'Folha de Ituiutaba',
            'data_publicacao': '10/10/1959',
            'cidade': 'Ituiutaba',
            'estado': 'MG',
            'descricao_jornal': '',
            'imagens': []
        }
        jornal = Jornal(dados_jornal)
        assert isinstance(jornal, Jornal)
        del(jornal)

    def test_valida_dados_jornal(self):

        # testando se o usuário colocou a data certa
        dados_jornal = {
            'titulo_jornal': 'Folha de Ituiutaba',
            'data_publicacao': '10/10/1959',
            'cidade': 'Ituiutaba',
            'estado': 'MG',
            'descricao_jornal': 'O jornal é teste!',
            'imagens': []
        }

        jornal = Jornal(dados_jornal)

        self.assertEqual(jornal.titulo_jornal, 'Folha de Ituiutaba')
        self.assertEqual(jornal.data_publicacao, '10/10/1959')
        self.assertEqual(jornal.cidade, 'Ituiutaba')
        self.assertEqual(jornal.estado, 'MG')
        self.assertEqual(jornal.descricao_jornal, 'O jornal é teste!')
        self.assertEqual(jornal.nome_arquivo,
                         '1959_10_10_folha_de_ituiutaba.pdf')

        del(jornal)

    def test_valida_data_publicacao_jornal(self):
        # testando se o usuário colocou a data errada
        dados_jornal = {
            'titulo_jornal': 'Folha de Ituiutaba',
            'data_publicacao': '31/02/1959',
            'cidade': 'Ituiutaba',
            'estado': 'MG',
            'descricao_jornal': ''	,
            'imagens': []

        }

        with self.assertRaises(ValueError):
            jornal = Jornal(dados_jornal)
            print('valor de data incorrero')
            del(jornal)

    def test_gera_arquivo_pdf_jornal_sem_ocr(self):
        lista_imagens = glob.glob(
            '/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1960_06_correio_do_pontal/*.JPG')
        dados_jornal = {
            'titulo_jornal': 'Correio do Pontal',
            'data_publicacao': '10/06/1960',
            'cidade': 'Ituiutaba',
            'estado': 'MG',
            'descricao_jornal': 'O jornal é teste!',
            'imagens': lista_imagens
        }
        jornal = Jornal(dados_jornal)
        jornal.gera_arquivo_jornal('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1960_06_correio_do_pontal/pdf')
        self.assertTrue(os.path.getsize(jornal.nome_arquivo) > 0.0)

    def test_gera_ocr(self):
        lista_imagens = glob.glob('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1960_06_correio_do_pontal/*.JPG')
        dados_jornal = {
            'titulo_jornal': 'Correio do Pontal',
            'data_publicacao': '10/06/1960',
            'cidade': 'Ituiutaba',
            'estado': 'MG',
            'descricao_jornal': 'O jornal é teste!',
            'imagens': lista_imagens
        }
        jornal = Jornal(dados_jornal)
        self.assertEqual(jornal.gera_ocr('/home/janderson/pesquisa_pibit/jornais/pendrive_cepdomp/1960_06_correio_do_pontal/pdf'), 0)
if __name__ == '__main__':
    unittest.main()

    # hangout com Kent Back sobre TDD
    # https://www.youtube.com/watch?v=z9quxZsLcfo
