from trabalhador import Trabalhador

class Coordenador:
    def __init__(self):
        self.matriz1 = [[1, 2, 0], [3, -1, 4], [2, 0, 1]]
        self.matriz2 = [[2, 1, 3], [0, 4, -1], [1, 2, 0]]
        self.resultado = [[" " for _ in range(3)] for _ in range(3)]

    def juntarMatriz(self, valor, par):
        self.resultado[par[0]][par[1]] = valor

def main():
    coordenador = Coordenador()
    trabalhador = Trabalhador()

    num_linhas_matriz1 = len(coordenador.matriz1)
    num_colunas_matriz2 = len(coordenador.matriz2[0])

    for indiceLinha in range(num_linhas_matriz1):
        for indiceColuna in range(num_colunas_matriz2):
            # 1. Obtém a linha inteira da matriz 1
            linha = coordenador.matriz1[indiceLinha]
            
            # 2. Extrai a coluna inteira da matriz 2
            coluna = [linha_m2[indiceColuna] for linha_m2 in coordenador.matriz2]
            
            # 3. Chama a função passando a linha, a coluna e o par ordenado (tupla)
            # Não preciso passar o par atualmente, mas vou precisar ao criar Threads
            valor, par = trabalhador.calcularValor(linha, coluna, (indiceLinha, indiceColuna))
            coordenador.juntarMatriz(valor, par)

    for linha in coordenador.resultado:
        print(linha)

if __name__ == "__main__":
    main()