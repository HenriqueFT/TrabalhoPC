import sys
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as linalg

#Pega os vetores b e x0 apartir do arquivo, e levanta erros.
def pegarVetores(f,linhas):

    b = []
    x0 = []

    b_len=0
    x0_len=0

    linha = f.readline() 

    while 1 :
        #Se ambos tiverem tamanho já temos ambos os vetores
        if b_len > 0 and x0_len > 0 : break

        #Se chegarmos numa linha vazia levantamos qual o erro e o programa para
        if linha == '':
            if b_len == 0:
                print('Não foi encontrado o vetor b.\n')
            if x0_len == 0:
                print('Não foi encontrado o vetor x0.\n')
            print('Verifique a entrada.\n')    
            sys.exit()
        
        #Atualizamos b 
        if linha == 'b\n':
            linha = f.readline()
            if linha != '' or linha != '\n':
                linha = linha.rstrip('\n')
                dados = linha.split()
                b_len = len(dados)
                b = np.fromstring(linha, dtype=int, sep=' ')

        #Atualizamos x0
        if linha == 'x0\n' or linha == 'x\n':
            linha = f.readline()
            if linha != '' or linha != '\n':
                linha = linha.rstrip('\n')
                dados = linha.split()
                x0_len = len(dados)
                x0 = np.fromstring(linha, dtype=int, sep=' ')
        
        #Vamos para a linha seguinte
        linha = f.readline()
    
    if b_len == x0_len and b_len == linhas :
        return b,x0 
    
    print ('Houve um erro.\nCheque se b e x0, e tem o mesmo comprimento que A.\n')


# Dado um sistema Ax = B, este metodo irá ler os dados e retornar uma matriz esparsa
def leituraDados(f):
    # primeira linha irá conter as dimensões da matriz A, esta linha é dada apenas por dois numeros
    # onde o primeiro é a qtd de linhas e o segundo é a qtd de colunas
    # a separação entre os números é feita por um espaço
    shape = f.readline().split()
    linhas = int(shape[0])
    colunas = int(shape[1])

    if linhas != colunas : 
        print('A matriz esparça deve ser NxN.\n Por favor, verifique a entrada.\n')
        sys.exit()

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
    print('\nLendo matriz A\n')
    for contador_linha in range(linhas):
        dados_linha = f.readline().split()

        # esta variavel é usada para fazer um controle dos elementos de indptr
        qtdElem = 0

        for contador_coluna in range(colunas):
            #Pulamos quando o dado é 0 
            if dados_linha[contador_coluna] == "0":
                continue
            # para cada elemento diferente de 0, atualizamos as listas data e indices
            data.append(int(dados_linha[contador_coluna]))
            indices.append(contador_coluna)
            qtdElem += 1

        # e ao final do loop atualizamos a lista indptr
        indptr.append(qtdElem + indptr[-1])

    A = sp.csr_matrix((data, indices, indptr), shape=(linhas, colunas)) 
    b = []
    x0 = []

    print('Lendo vetores b e x0\n')
    b,x0 = pegarVetores(f,linhas)

    return A,b,x0