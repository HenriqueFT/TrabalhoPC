import warnings

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as linalg

warnings.filterwarnings("ignore")

def GMRes(A, b, x0, nmax_iter):
    t1 = A.dot(x0)
    r = b - t1

    x = []
    q = sp.csr_matrix((nmax_iter, A.shape[0]), dtype=float)
    x.append(r)
    q[0] = r / np.linalg.norm(r)

    h = sp.csr_matrix((nmax_iter + 1, nmax_iter), dtype=float)

    for k in range(min(nmax_iter, A.shape[0])):
        y = A.dot(q[k].transpose())

        for j in range(k + 1):
            h[j, k] = q[j].dot(y)[0,0]
            y = y - h[j, k] * q[j].transpose()
        h[k + 1, k] = linalg.norm(y)
        if h[k + 1, k] != 0 and k != nmax_iter - 1:
            q[k + 1] = (y / h[k + 1, k]).transpose()

        b = [0] * (nmax_iter + 1)
        b[0] = np.linalg.norm(r)

        result = linalg.lsqr(h, b)[0]

        x.append(q.transpose().dot(result) + x0)

    return x


def leituraDados(filename):
    # dado um sistema Ax = B, este metodo irá ler os dados e retornar uma matriz esparsa
    f = open(filename, 'r')

    # primeira linha irá conter as dimensões da matriz A, esta linha é dada apenas por dois numeros
    # onde o primeiro é a qtd de linhas e o segundo é a qtd de colunas
    # a separação entre os números é feita por um espaço
    shape = f.readline().split()
    linhas = int(shape[0])
    colunas = int(shape[1])

    # Estas 3 listas são os dados necessários para instanciar uma csr_matrix da biblioteca scipy
    # data contém os dados diferentes de 0
    data = []
    # indices contém os indices das colunas onde cada dado se encontra
    # de forma que o dado data[i] encontra-se na coluna indices[i]
    indices = []
    # indptr contém os slices para identificar em qual linha encontra-se cada elemento
    # para mais informações sobre este dado, este link contém uma explicação
    # https://stackoverflow.com/questions/52299420/scipy-csr-matrix-understand-indptr
    indptr = [0]

    # iterando sobre cada linha da matriz na coluna
    for contador_linha in range(linhas):
        dados_linha = f.readline().split()

        # esta variavel é usada para fazer um controle dos elementos de indptr
        qtdElem = 0

        for contador_coluna in range(colunas):
            if dados_linha[contador_coluna] == "0":
                continue
            # para cada elemento diferente de 0, atualizamos as listas data e indices
            data.append(int(dados_linha[contador_coluna]))
            indices.append(contador_coluna)
            qtdElem += 1

        # e ao final do loop atualizamos a lista indptr
        indptr.append(qtdElem + indptr[-1])

    resultado = np.fromstring(f.readline(), dtype=int, sep=' ')
    return sp.csr_matrix((data, indices, indptr), shape=(linhas, colunas)), resultado


A, b = leituraDados("matriz.txt")
x0 = np.array([0,0,0,0,0,0,0,0,0,0])
print("Resultado = ", GMRes(A, b, x0, 10)[-1])