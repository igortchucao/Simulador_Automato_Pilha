
# SIMULADOR DE AUTOMATOS FINITOS

Pré-requisito para execução do simulador é a versão 3.6 ou superior do Python.

```
$ python3 --version
```

Como resultado desejado deve aparecer algo do como:

```
Python 3.7.0
```

Para a execução do script basta especificar um arquivo .txt para a simulação contendo o autômato.

O arquivo deve seguir o seguinto modelo:

```
afd       # Especificação do autômato.
2         # Quantidade de estados
01        # Alfabeto
q0        # Estado Inicial
q1        # Estado Final
q0 0 q0   # Tabela de transição
q0 1 q1
q1 0 q1
q1 1 q1
```
Caso no arquivo não possua uma transição será considerada como inexistente. (e.g. δ(qi, w) = qi)

Para criar um autômato no simulador:
```
$ python3.6 main.py
```

Para executar o AFD de exemplo:
```
$ python3.6 main.py afd.txt
```

Para executar o AFN de exemplo:
```
$ python3.6 main.py afn.txt
```
