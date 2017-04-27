"""
Autor: Janderson de Almeida Coelho da Silva
Data de Modificação: 24/01/2017

Este módulo será responsável para a execução do processo de criação
de documentos digitalizados com reconhecimento óptico de caracteres
Aqui têm-se as classes que serão utilizadas para atender os casos de 
uso de :

	-> Preprocessamento digital das imagens digitalizadas dos documentos usando OpenCV e scikit-image 
	->  


"""

#para ler com calma:
#https://awesomelemon.github.io/2017/01/15/Document-recognition-with-Python-OpenCV-and-Tesseract.html

from transform import four_point_transform
import imutils
from skimage.filters import threshold_adaptive
import numpy as np
import cv2
import pytesseract
from PIL import Image
import os
import subprocess

class Imagem(object):
	"""
	Classe que preprocessa as imagens antes de criar o OCR
	Atributos:
	-> imagem: Imagem digitalizada para ser preprocessada. 
	           No momento ela recebe imagens JPEG

	-> original_shape: Tupla que possui a resolução original da imagem
	-> ratio: Valor que terá um tamanho reduzido da imagem original para 
	          melhoria de desempenho do preprocessamento.
	-> orig:  cópia do objeto que representa a imagem original com o  propósito de evitar inconsistências no resultado final do preprocessamento
	-> gray: imagem convertida para escala de cinza. 
	-> blur: imagem borrada para otimizar o processo de binarização e melhor reconhecimento dos caracteres futuramente
	-> edged: imagem vetorizada com o algoritmo de Canny. Será útil para encontrar as bordas do documento
	-> contornos: array que possui as coordenadas das bordas detectadas do documento			
	-> warped: imagem com as bordas recortadas e em preto e branco. Até o momento foi a melhor forma encontrada 
	           para o OCR do Tesseract trabalhar.

	"""
	def __init__(self, arquivo_imagem=None):

		""" 
		Método construdor da classe. Instancia a imagem para ser preprocessada
		Exemplo de uso:

		>>> im = Imagem('IMG_1642.JPG')
		"""
		if arquivo_imagem != None:

			self.imagem         = cv2.imread(arquivo_imagem)
			self.imagem         = self.make_border(self.imagem.copy())
			self.original_shape = self.imagem.shape
			self.ratio          = self.imagem.shape[0] / 600.0
			self.orig           = self.imagem.copy()
			self.imagem         = imutils.resize(self.imagem, height = 600)
			self.gray           = cv2.cvtColor(self.imagem, cv2.COLOR_BGR2GRAY)
			self.blur           = cv2.GaussianBlur(self.gray, (5, 5), 0)
			self.edged          = cv2.Canny(self.blur, 40, 150)
			self.contornos      = self.encontra_contornos()
			self.warped 		= self.__recorta_bordas()

		else:
			pass


	def make_border(self,img):
		""" 
		Cria cria uma borda em volta do documento digitalizado.
		Seu objetivo é ajudar o método de detecção de bordas, pois
		às vezes o algoritmo que faz isso não "acerta" as bordas externas
		da imagem.
		Este método é executado dentro do método construtor da classe:

		Exemplo de uso:

		>>> from imagem import Imagem
		>>> im = Imagem('IMG_1642.JPG')
		>>> im = im.make_border(im.imagem.copy())


		"""
		rows,cols = img.shape[:2]
		dst = img.copy()
		top = int (0.06*rows)
		bottom = int (0.06*rows)
		left = int (0.06*cols)
		right = int (0.06*cols)
		color = (0,0,0) # cor preta para aprimorar a busca de borda do documento
		dst = cv2.copyMakeBorder(img,top,bottom,left,right,cv2.BORDER_CONSTANT,value = color)
		return dst

	def encontra_contornos(self):
		"""
		Encontra as coordenadas das bordas externas da imagem e grava em um array. Esse método está descrito melhor na URL
		http://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/

		Exemplo:
		
		>>> from imagem import Imagem
		>>> im = Imagem('IMG_1642.JPG')
		>>> contornos = im.encontra_contornos()
		>>> print(contornos)

		"""
		(_, cnts, _) = cv2.findContours(self.edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
		for c in cnts:
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.02 * peri, True)
			if len(approx) == 4:
				screenCnt = approx
				break
		return screenCnt


	def __recorta_bordas(self):
		"""
		Recorta as bordas externas da imagem que foi colocada para aprimorar o preprocessamento.
		Uso exclusivo da classe não podendo ser chamada externamente.	
			
		"""
		warped = four_point_transform(self.orig, self.contornos.reshape(4, 2) * self.ratio)
		warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)		
		warped = threshold_adaptive(warped,251, 'gaussian', offset = 20)
		warped = warped.astype("uint8") * 255		
		return warped

	def salvar_imagem_processada(self, tipo_imagem=("CO", "BI", "EC"),nome_arquivo=str):

		
		if tipo_imagem == "CO":
			imagem_processada = four_point_transform(self.orig, self.contornos.reshape(4, 2) * self.ratio)
			imagem_processada = imutils.resize(imagem_processada, height = self.original_shape[0])
			cv2.imwrite(nome_arquivo, imagem_processada,  [cv2.IMWRITE_JPEG_QUALITY, 100])
			return True
		
		elif tipo_imagem == "EC":
			imagem_processada = four_point_transform(self.orig, self.contornos.reshape(4, 2) * self.ratio)
			imagem_processada = imutils.resize(imagem_processada, height = self.original_shape[0])
			imagem_processada = cv2.cvtColor(imagem_processada, cv2.COLOR_BGR2GRAY)
			cv2.imwrite(nome_arquivo, imagem_processada,  [cv2.IMWRITE_JPEG_QUALITY, 100])
			return True

		elif tipo_imagem == "BI":
			cv2.imwrite(nome_arquivo,self.warped,  [cv2.IMWRITE_JPEG_QUALITY, 100])	
			return True		
		else:
			print("Tipo inválido de imagem")
			return False			
			

	# def mostra_imagem(self):
	# 	cv2.imshow("Imagem com borda", self.imagem)
	# 	cv2.imshow("Imagem em cinza", self.gray)
	# 	cv2.imshow("Imagem vetorizada", self.edged)
	# 	cv2.imshow("Imagem redimensionada", self.warped)
	# 	cv2.waitKey(0)
	# 	cv2.destroyAllWindows()

	def gera_arquivo_texto(self, arquivo_imagem=str, arquivo_texto=str, idioma=str):

		texto_ocr = pytesseract.image_to_string(Image.open(arquivo_imagem), lang=idioma)
		arq = open(arquivo_texto,"w")
		arq.write(texto_ocr)
		arq.close


	def gera_pdf(self,arquivo_imagem):
		os.system("tesseract %s -l %s -psm 5 %s pdf" %(arquivo_imagem, idioma, arquivo_imagem[:-4]))

	
	def compacta_pdf(self, pdf_input, pdf_output):
		arquivo_saida = '-sOutputFile=c_'+ pdf_output
		subprocess.Popen(['/usr/bin/gs', 
						 '-sDEVICE=pdfwrite',
						 '-dCompatibilityLevel=1.4', 
						 '-dPDFSETTINGS=/ebook',
						 '-dColorConversionStrategy=/LeaveColorUnchanged',
						 '-dAutoRotatePages=/None',		
						 '-dColorImageDownsampleType=/Bicubic',
						 '-dColorImageResolution=90',
						 '-dGrayImageDownsampleType=/Bicubic',
						 '-dGrayImageResolution=90',
						 '-dMonoImageDownsampleType=/Bicubic',
						 '-dMonoImageResolution=90',
						 '-dNOPAUSE', '-dBATCH',  '-dQUIET', 
						 pdf_output, pdf_input], stdout=subprocess.PIPE)