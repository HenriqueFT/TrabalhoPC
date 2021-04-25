import warnings
import numpy as np

import gmres as g 
import leitura as l

warnings.filterwarnings("ignore")

filename = input("Por favor dê o nome do arquivo: ")

try:
    f = open(filename, 'r')
except: 
    print('Não foi encontrado o arquivo\nIremos utilizar o arquivo matrix.txt\n')
    f = open('matriz.txt', 'r')

A, b, x0 = l.leituraDados(f)

print("Resultado = ", g.GMRes(A, b, x0, 12)[-1])