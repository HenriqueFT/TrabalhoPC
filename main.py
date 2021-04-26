import warnings
import numpy as np

import gmres as g 
import leitura as l
import time 

warnings.filterwarnings("ignore")

'''
filename = input("Por favor dê o nome do arquivo: ")

try:
    f = open(filename, 'r')
except: 
    print('Não foi encontrado o arquivo\nIremos utilizar o arquivo matrix.txt\n')
    f = open('matriz.txt', 'r')
'''
f = open('matriz2.txt', 'r')

A, b, x0, n_iteracoes = l.leituraDados(f)

timeStart = time.time()

print("Resultado = ", g.GMRes(A, b, x0, n_iteracoes)[-1])

timeEnd = time.time()

print("\nO tempo de processamento foi de",timeEnd-timeStart,'segundos\n')