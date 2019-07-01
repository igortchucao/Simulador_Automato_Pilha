#-*- coding: utf-8 -*-
import sys
import automatos

def main():
	"""
	Verifica se o arquivo foi especificado no comando de execução do
	programa. Senão, a opção de criar um autômato será escolhida por
	padrão.
	Caso o arquivo não seja encontrado, uma mensagem de erro será mostrada.

	Para a criação de um autômato será requisitado o alfabeto, a quantidade
	de estados e o estado inicial.
	Então será definido se o autômato é um AFD ou AFN. E, para cada um, seus
	respectivos métodos.
	"""
	try:
		arquivo = sys.argv[1]
		automatos.le_arquivo(arquivo)
	except IndexError:
		i = True
		alfabeto = input('Entre com o alfabeto: ')
		qtd_estados = int(input('Digite a quantidade de estados: '))
		lista_estados = automatos.criar_estados(qtd_estados)
		
		automatos.setInicial(lista_estados)

		menu = input('AFD ou AFN? ')
		if menu.upper() == 'AFD':
			automatos.setTransicaoAFD(lista_estados, alfabeto)
			automatos.setFinal(lista_estados)
			while i == True:
				palavra = automatos.getPalavra(alfabeto)
				print('A palavra', palavra, automatos.processa_palavraAFD(lista_estados, palavra), 'pelo autômato')
				sair = input('Sair? (S/N) ')
				i = False if sair.upper() == 'S' else True
		elif menu.upper() == 'AFN':
			automatos.setTransicaoAFN(lista_estados, alfabeto)
			automatos.setFinal(lista_estados)
			while i == True:
				palavra = automatos.getPalavra(alfabeto)
				print('A palavra', palavra, automatos.processa_palavra(lista_estados, palavra), 'pelo autômato')
				sair = input('Sair? (S/N) ')
				i = False if sair.upper() == 'S' else True
		else:
			print('Palavra invalida')

	except FileNotFoundError:
		print('Arquivo não encontrado')

if __name__ == '__main__':
    main()
