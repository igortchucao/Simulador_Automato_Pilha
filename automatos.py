#-*- coding: utf-8 -*-

class Estado:
	"""
	A classe estado possui os seguintes atributos:
	nome -> identificação do estado
	transicao -> dicionário contendo os símbolos do alfabeto e suas respectivas transições
	final -> indicativo de estado final
	inicial -> indicativo de estado inicial
	"""
	def __init__(self, nome):
		self.nome = nome
		self.transicao = {}
		self.final = False
		self.inicial = False

def le_arquivo(arquivo):
	"""
	O formato do arquivo deve respeitar a seguinte ordem:
	*Tipo do atômato
	*Quantidade de estados
	*Alfabeto
	*Estado inicial
	*Estado final
	*Transições

	As transições devem respeitar a seguinte configuração:
	Origem Símbolo Destino (para AFD)
	ex.: q0 0 q0

	Origem Símbolo Destinos (para AFN)
	ex.: q0 a q1 q2

	Caso determinado estado não processe um síbolo, não é
	necessário especificar a transição no arquivo. Caso o
	seja feito, deve seguir o exemplo.
	ex.: 'q0 b '
	"""
	with open(arquivo, 'r') as f:
		tipo = f.readline().split()
		qtd_estados = f.readline().split()
		alfabeto = f.readline().split()
		lista_estados = criar_estados(int(qtd_estados[0]))

		# definindo estado inicial
		linha = f.readline().split()
		for e in lista_estados:
			if e.nome == linha[0]:
				e.inicial = True

		# definindo estado final
		linha = f.readline().split()
		for e in lista_estados:
			if e.nome == linha[0]:
				e.final = True

		# recebendo todas as transições
		# transicao = f.readline().split()
		# q0 a * B q0
		# [0] = estado; [1] = simbolo; [2] = desempilha; [3] = empilha; [4:] = destinos
		for transicao in f:
			tupla = ()
			t = transicao.split()
			for e in lista_estados:
				if e.nome == t[0]:
					tupla = ((t[4:], t[2], t[3]))
					# exemplo: (['q0'], '*', 'B') 
					e.transicao.update({t[1]: tupla})
				#print(e.transicao)
	f.close()
	
	sair = True
	while sair:
		palavra = input('Palavra a ser processada: ')
		resultado = processa_palavraAFN(lista_estados, palavra)
		print('A palavra', palavra, resultado, 'pelo', tipo[0])
		i = input('Sair? (S/N) ')
		sair = (False) if i.upper() == 'S' else (True)

def criar_estados(qtd_estados):
	"""
	Criação de um dicionário auxiliar com todos os símbolos do alfabeto.
	Inicialmente, todos os estados levam à um estado "vazio",
	independente de qual símbolo tenha sido processado.
	"""
	estados = []
	for i in range(0, qtd_estados):
		nome = 'q' + str(i)
		estados.append(Estado(nome))

	return estados

def setTransicaoAFD(lista_estados, alfabeto):
	"""
	Recebe o alfabeto e define, para cada estado, a transição do mesmo,
	o que será desempilhado e o que será empilhado.
	Por se tratar de um AFD, cada símbolo processado só leva à um único
	estado, desempilhará e empilhará somente um simbolo
	"""

	for estado in lista_estados:
		for simbolo in alfabeto:
			index = input(estado.nome + '--' + simbolo + '-->')
			empilha = input('Empilha algo?')
			desempilha = input("Desempilha algo?")

			estado.transicao[simbolo] = (index, desempilha, empilha)

def setTransicaoAFN(lista_estados, alfabeto):
	"""
	Recebe o alfabeto e define, para cada estado, a transição do mesmo.
	Por se tratar de um AFN, cada símbolo pode levar a mais de um estado.
	A lista "estadosMudanca" é responsável por armazenar os estados destinos e
	posteriormente adicionada ao dicionário de transição.
	A lista "empilhadores" é responsavel por armazenar o que será empilhado
	quando o estado atual ler o determinado alfabeto.
	E a lista "desempilhadores" o que será retirado da pilha.
	"""
	estadosMudanca = []
	empilhadores = []
	desempilhadores = []

	for estado in lista_estados:
		for simbolo in alfabeto:
			estadosMudanca.clear()
			while True:
				index = input(estado.nome + '--' + simbolo + '-->')
				empilha = input('Empilha algo?')
				desempilha = input("Desempilha algo?")

				estadosMudanca.append(index)
				empilhadores.append(empilha)
				desempilhadores.append(desempilha)

				if input('Adicionar mais estados? (S/N) ').upper() == 'N':
					break
			estado.transicao[simbolo] = (estadosMudanca.copy(), empilhadores.copy(), desempilhadores.copy())

def setInicial(estados):
	"""
	Lista inicialmente todos os estados existentes
	O usuário entra com a id ".nome" do estado desejado
	"""
	for e in estados:
		print('Estado:', e.nome)

	Teste = False
	while(Teste == False):
		index = input('Qual estado inicial? ')
		for e in estados:
			if (e.nome == index):
				e.inicial = True
				Teste = True
		if Teste == False:
			print('Estado inexistente')

def setFinal(estados):
	"""
	AFDs/AFNs podem ter mais de um estado final
	Sendo assim, é requerido uma quantidade para definir o loop
	"""
	qtd = int(input('Quantidade de estados finais:'))

	if qtd > len(estados):
		print("Quantidade maior do que a de estados existentes")
		while qtd > len(estados):
			qtd = int(input('Quantidade de estados finais:'))


	for i in estados:
		print('Estado:',i.nome)
	while qtd != 0:
		nome = input('Estado final:')
		for e in estados:
			if e.nome == nome and e.final == True:
				print('O estado', e.nome, 'já é um estado final')
			elif e.nome == nome and e.final == False:
				e.final = True
				qtd -= 1

def getPalavra(alfabeto):
	"""
	Recebe a palavra a ser processada pelo Autômato,
	caso contenha símbolos diferente do alfabeto, a palavra não
	será aceita
	"""
	i = True
	while i:
		palavra = input('Digite a palavra a ser preocessada: ')
		for simb in palavra:
			if alfabeto.count(simb) == 0:
				print('A palavra contém símbolos não existentes no alfabeto')
			else:
				i = False
	return palavra

def processa_palavra(pilha, lista_estados, palavra):
	"""
	Procura o estado inicial na lista de estados e o adiciona à lista
	de estados ativos.
	Para cada símbolo da palavra a ser processada, enquanto existirem
	estados ativos, verificar se o símbolo leva à algum estado. Se levar,
	adicioná-lo à fila de processamento, que, posteriormente, será incorporada
	como estados ativos.
	Se algum estado da lista de estados ativos final possuir o atributo ".final"
	igual à "True", então a palavra é aceita pelo autômato.

	"""
	e_atual = None
	# Procurando o estado inicial
	for e in lista_estados:
		if e.inicial == True:
			e_atual = e

	e_ativos = []
	e_ativos.append(e_atual)
	fila_proc = []

	for simb in palavra:
		while len(e_ativos) > 0:
			# Verificando se o estado ativado por 'simb' em 'e_atual'
			# é diferente de vazio. Se sim, colocá-los como estados ativos
			e_atual = e_ativos.pop()
			if e_atual.transicao.get(simb) is not None:
				for nome_estado in e_atual.transicao.get(simb):
					# Adicionar o elemento q possui o 'nome'especificado
					for e in lista_estados:
						if e.nome == nome_estado:
							fila_proc.append(e)
		e_ativos = fila_proc.copy()
		fila_proc.clear()

	for estado in e_ativos:
		if estado.final == True:
			return 'é aceita'
	return 'não é aceita'

def processa_palavraAFD(lista_estados, palavra):
	"""
	Procura o estado inicial na lista de estados e o torna estado atual.
	E, para cada símbolo da palavra, verificar qual estado destino e torná-lo
	o atual.
	Se no final da palavra ".final" for "True", então a palavra é aceita pelo
	autômato.
	"""
	pilha = []
	e_atual = None
	# Busca o estado inicial
	for e in lista_estados:
		if e.inicial == True:
			e_atual = e
	# Para cada símbolo da Palavra
	# verificar qual estado é ativado e torná-lo o estado atual
	for simb in palavra:
		nome_prox = e_atual.transicao[simb][0]

		# Se o pedido que é feito para desempilhar não é aceito
		# a palavra pode ser rejeitada pelo automato
		if(e_atual.transicao[simb][1] != '*'):
			#Se tiver algum simbolo na pilha
			if(len(pilha) > 0):
				#Se o valor para desempilhar for igual ao topo da pilha
				if(e_atual.transicao[simb][1] == pilha[-1]):
					del(pilha[-1])
				else:
					return 'não é aceita'
			else:
				return 'não é aceita'

		# Empilha 
		if(e_atual.transicao[simb][2] != '*'):
			pilha.append(e_atual.transicao[simb][2])

		for e in lista_estados:
			if e.nome == nome_prox:
				e_atual = e

	# Se o ultimo estado possuir o atributo '.final' = true, então
	# a palavra é aceita
	if(len(pilha) == 0):
		return 'é aceita' if e_atual.final is True else 'não é aceita'
	return 'não é aceita'

def processa_palavraAFN(lista_de_estados, palavra):
	pilha = []
	e_atual = Estado('a')
	# Busca o estado inicial
	for e in lista_de_estados:
		if e.inicial == True:
			e_atual = e
	# Lista de estados ativos no afn
	e_ativos = []
	e_ativos.append(e_atual)

	# Fila dos próximos estados a serem ativados
	fila_prox = []

	# Verificando se o movimento vazio é aceito no estado inicial
	if e_atual.transicao['*'] is not None:
		nome_estado = e_atual.transicao['*'][0]
		for prox_estado in nome_estado:
			for e in lista_de_estados:
				if e.nome == prox_estado:
					e_ativos.append(e)
	
	# Percorrendo a palavra
	for simb in palavra:
		#
		print('\nEstados ativos: ',end='')
		for e in e_ativos:
			print(e.nome,'', end='')
		print()
		#
		for e_atual in e_ativos:
			print(e_atual.nome,'Lendo:',simb)

			# Acrescentado os estados a serem ativados
			# Se estado atual possuir transições
			if len(e_atual.transicao.keys()) > 0:
				# Se possuir transição *
				if e_atual.transicao['*'] is not None:
					nome_estado = e_atual.transicao['*'][0]
					print('Transição * =>', nome_estado)
					for prox_estado in nome_estado:
						for e in lista_de_estados:
							if e.nome == prox_estado:
								fila_prox.append(e)
				
				# Se possuir transição referente ao símbolo lido
				keys_da_transicao = []
				for i in e_atual.transicao.keys():
					keys_da_transicao.append(i)
				if keys_da_transicao.count(simb) != 0:
					nome_estado = e_atual.transicao[simb][0]
					print('Transição', simb,'=>', nome_estado)
					for prox_estado in nome_estado:
						for e in lista_de_estados:
							if e.nome == prox_estado:
								fila_prox.append(e)

					# Desempilhar
					if(e_atual.transicao[simb][1] != '*'):
						# Se ao tentar desmpilhar houver falha, parar o processamento
						# Se tiver algum simbolo na pilha
						if(len(pilha) > 0):
							#Se o valor para desempilhar for igual ao topo da pilha
							if(e_atual.transicao[simb][1] == pilha[-1]):
								pilha.pop()
						else:
							return 'não é aceita'

					# Empilha o que não for *
					if(e_atual.transicao[simb][2] != '*'):
						pilha.append(e_atual.transicao[simb][2])

				print('Pilha:', pilha)
			# Copiando a tlista de próximos estados para estados ativos
		e_ativos = fila_prox.copy()
		fila_prox.clear()

	# Adicionando os estados ativáveis por movimento vazio a partir dos estados finais
	e_finais = []
	for e in e_ativos:
		if len(e.transicao) > 0:
			if e.transicao['*'] is not None:
				estados_ativados = e.transicao['*'][0]
				for prox_estado in estados_ativados:
					for est in lista_de_estados:
						if est.nome == prox_estado:
							e_finais.append(est)
		else:
			e_finais = e_ativos.copy()
			e_ativos.clear()
	# Se o ultimo estado possuir o atributo '.final' = true, então
	# a palavra é aceita
	if(len(pilha) == 0):
		for estado in e_finais:
			if estado.final == True:
				return 'é aceita'
	return 'não é aceita'
