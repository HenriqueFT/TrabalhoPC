import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as linalg
import pandas as pd

# Não é necessaria e esta comentada no codigo com '##', 
# que podem ser retirados para ver o processo sendo feito aos poucos.
# Se eh recomendado utilizar o modo debug para poder controlar a progressao do algoritmo eacompanhar.
def print_m(matriz):
    df = pd.DataFrame(matriz.toarray())
    print(df,'\n')

# Aceita como input matrizes com 1 (vetor) ou 2 "coordenadas" (dimensoes)
# Para matrizes, essa funcao executa a norma de Frobenius.
# Para vetores, essa funcao usa a forma Euclidiana (a de distancia).
# Que funciona de forma igual entre matrizes e vetores, retornando um float
def n_norm(blob):
    return np.linalg.norm(blob)

# Apenas aceita matrizes esparsar, cai num caso especifico q n_norm levanta um erro, de resto faz o mesmo.
def s_norm(matriz):
    return linalg.norm(matriz)

def GMRes(A, b, x0, nmax_iter):
    # Começamos fazendo uma multiplicao entre a matriz 'A' e o vetor 'x0' resultando em 't1'
    # Fazemos a diferença entre os vetores 'b' e 't1'
    t1 = A.dot(x0)
    r = b - t1

    # Aqui iniciamos um vetor de comprimento <numero de interacoes> + 1 
    # O qual sua primeira posição conteráo valor da norma de 'r'
    p = [0] * (nmax_iter + 1)
    p[0] = n_norm(r)

    # Aqui iniciamos duas variaveis 'x' e 'q' 
    # 'x' recebe o vetor resultante de  b - t1
    # 'q' eh uma matriz esparsa de dimensoes <numero de interacoes>x<N> 
    # Por fim colocamos na primeira linha de 'q' o vetor resultante de r / n_norm
    x = []
    q = sp.csr_matrix((nmax_iter, A.shape[0]), dtype=float)
    x.append(r)
    q[0] = r / n_norm(r)

    # Por ultimo iniciamos uma matriz esparsa de dimensoes (<numero de interacoes>+1)x(<numero de interacoes>)
    h = sp.csr_matrix((nmax_iter + 1, nmax_iter), dtype=float)

    # Aqui é onde a parte principal da função
    # Fazemos 2 for um dentro do outro: 
    #   O primeiro tendo a variavel 'k' de 0 ao indo do menor valor entre o número de interacoes e 'N'
    #   O segundo tendo a variavel 'j' indo de 0 ateh k + 1 
    for k in range(min(nmax_iter, A.shape[0])):
        # Começamos iniciando um vetor y que é o resultado do produto entre A e q 
        # Observe que q é trasposta apenas para possibilitar a multiplicacao entre o vetor e a matriz
        # E observe que y inicia tendo q[0] como r / n_norm(r)
        y = A.dot(q[k].transpose())

        # Aqui fazemos um loop que vai de 0 ateh k 
        # 1-Atualizamos o valor em h[j,k] com o valor de q[j].dot(y)[0,0] 
        #   Note que q[j] vai apenas ateh onde preenchemos ele, entao ir ateh 'k' eh o ideal
        #   Multiplicamos os 2 arrays, que resulta em um array de uma posição (por isso pegamos [0,0])
        # 2-Atualizamos 'y' diminuindo 'y' pelo vetor resultado de 'q[j].dot(y)'
        # Vamos atualizando cada coluna 'k' na posição 'j'  
        for j in range(k + 1):
            h[j, k] = q[j].dot(y)[0,0]
            y = y - h[j, k] * q[j].transpose()

            ##print_m(h)

        # Por fim colocamos o valor da norma de y, na última posicao nao nula dda coluna 'k' 
        h[k + 1, k] = s_norm(y)

        ##print_m(h)
        ##print_m(q)
        
        # Enquanto a norma de 'y' não for 0, isto é um vetor nulo, e 'k' nao estiver na ultima posicao de 'q', 
        #   uma vez que isso levaria a 'index out of bounds'
        # Guardamos os dados de um array resultante na posição seguinte de 'q' 
        # esta contendo o vetor 'y' dividido por sua norma. O qual serah utilizado na proxima iteracao do for
        if h[k + 1, k] != 0 and k != nmax_iter - 1:
            q[k + 1] = (y / h[k + 1, k]).transpose()

        # LSQR resolve equacoes do tipo Ax = b , sendo A uma matriz esparsa e b um vetor
        # Ela se utiliza de metodos iterativos para resolver este problemas
        # Por fim pegamos o primeiro resultado
        result = linalg.lsqr(h, p)[0]

        # Ao fim da iteracao nos colocamos um array a mais em 'x' sendo este a multiplicacao da 
        # transposta de 'q' com o resultado e depois somamos o vetor 'x0' 
        x.append(q.transpose().dot(result) + x0)

    return x