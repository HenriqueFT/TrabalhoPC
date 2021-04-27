# Trabalho de Programação Científica

Trabalho para a matéria de Programação Científica 2020-2, lidando com problema do tipo GMRES

## Tema

Resolução de problemas GMRes

## Como rodar o programa

1. Entrar na pasta do projeto.
2. Tendo [python 3](https://www.python.org/downloads/) instalado se abre o terminal e entra o comando os comandos:
   1. Linux:
     1. `pip install -r requirements.txt`
     2. `python main.py` ou `python3 main.py` (Caso já tenha uma versão de python anterior a 3 instalada)
   2. Windows:
     1. `py -m pip install -r requirements.txt`
     2. `py main.py`
3. Depois especifique o nome do arquivo de texto que será utilizado como entrada. O projeto já vem com 2 exemplos (matriz.txt e matriz2.txt) o primeiro sendo o utilizado no exemplo pelo professor e o segundo sendo uma matriz não simétrica (ambas esparsas).

### Como criar sua própria entrada

- Utilizemos como exemplo a entrada em matriz.txt

10  10  12\
4  1  -1  0  0  0  0  0  0  0\
1  4  1  -1  0  0  0  0  0  0\
-1  1  4  1  -1  0  0  0  0  0\
0  -1  1  4  1  -1  0  0  0  0\
0  0  -1  1  4  1  -1  0  0  0\
0  0  0  -1  1  4  1  -1  0  0\
0  0  0  0  -1  1  4  1  -1  0\
0  0  0  0  0  -1  1  4  1  -1\
0  0  0  0  0  0  -1  1  4  1\
0  0  0  0  0  0  0  -1  1  4\
b\
4  5  4  4  4  4  4  4  5  4\
x\
0  0  0  0  0  0  0  0  0  0

- Começamos com a número de linhas e colunas (NxN) da matriz, separados por 1 espaço (10 10)
- Logo depois vem o número de iterações nas quais o programa passará (12).
- Depois colocamos a matriz esparsa das dimensões dadas na primeira linha. Tendo o cuidado de separar cada número com 1 espaço, e quebrar linha seguindo o formato da matriz
- Na linha abaixo colocamos o caracter 'b' sozinho, para na linha seguinte colocar um vetor de N números espaçados por 1 espaço.
- Embaixo fazendo o mesmo colocando 'x' ou 'x0', seguido de outro vetor de N números esparsados por 1 espaço

## Estrutura

1. main.py : Concentrar todos os demais e rodar de forma simples, escolhendo como vamos enviar o problema e tendo contato com o usuário.
2. Leitura de entrada do problema resultando em uma matriz esparsa.
3. Aplicação do método de **GMRES** que recebe a matriz vinda da **main.py**.

## Bibliotecas externas

- [NumPy](https://numpy.org/) : Leitura de vetores vindos de um arquivo e fazer contas da norma de uma matriz. É utilizado em várias bibliotecas do SpiPy, especialmente a scipy.sparse
- [scipy.sparse](https://docs.scipy.org/doc/scipy/reference/sparse.html) : Para a criação e manipulação (principalmente transposição) de matrizes esparsas.
- [scipy.sparse.linalg](<https://docs.scipy.org/doc/scipy/reference/sparse.linalg.html#module-scipy.sparse.linalg>) : Para fazer álgebra nas matrizes esparsas.
- [pandas](https://pandas.pydata.org/docs/) : Imprimir matrizes de forma mais organizada e bonita.
  
