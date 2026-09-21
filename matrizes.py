"""Dados e funções utilitárias compartilhadas entre a Parte 1 e a Parte 2."""

MATRIZ_A = [[1, 2, 0], [3, -1, 4], [2, 0, 1]]
MATRIZ_B = [[2, 1, 3], [0, 4, -1], [1, 2, 0]]

# Tempo (s) que cada trabalhador "gasta" por célula. Serve só para tornar
# visível a diferença entre síncrono e assíncrono com matrizes pequenas.
ATRASO = 0.3


def extrair_coluna(matriz, indice_coluna):
    """Devolve a coluna `indice_coluna` da matriz como uma lista."""
    return [linha[indice_coluna] for linha in matriz]


def criar_resultado_vazio(matriz_a, matriz_b):
    """Cria a matriz resultante (linhas de A x colunas de B)."""
    return [[" " for _ in range(len(matriz_b[0]))] for _ in range(len(matriz_a))]


def imprimir_matriz(matriz, titulo="Resultado"):
    print(f"\n{titulo}:")
    for linha in matriz:
        print("  ", linha)


def multiplicar_sequencial(matriz_a, matriz_b):
    """Referência sequencial, usada para conferir se o resultado distribuído está certo."""
    return [[sum(a * b for a, b in zip(l, extrair_coluna(matriz_b, j)))
             for j in range(len(matriz_b[0]))] for l in matriz_a]