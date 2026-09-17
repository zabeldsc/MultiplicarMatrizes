from trabalhador import Trabalhador
from concurrent.futures import ThreadPoolExecutor, as_completed
class Coordenador:
    def __init__(self):
        self.matrizA = [[1, 2, 0], [3, -1, 4], [2, 0, 1]]
        self.matrizB = [[2, 1, 3], [0, 4, -1], [1, 2, 0]]
        self.resultado = [[" " for _ in range(len(self.matrizB[0]))] for _ in range(len(self.matrizA))]

    def juntarMatriz(self, valor, par):
        self.resultado[par[0]][par[1]] = valor

if __name__ == "__main__":
    coordenador = Coordenador()
    trabalhador = Trabalhador()

    num_linhas_matrizA = len(coordenador.matrizA)
    num_colunas_matrizB = len(coordenador.matrizB[0])

    max_threads = min(32, num_linhas_matrizA * num_colunas_matrizB)
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []

        for indiceLinha in range(num_linhas_matrizA):
                for indiceColuna in range(num_colunas_matrizB):
                    # 1. Obtém a linha inteira da matriz 1
                    linha = coordenador.matrizA[indiceLinha]
                    
                    # 2. Extrai a coluna inteira da matriz 2
                    coluna = [linha_m2[indiceColuna] for linha_m2 in coordenador.matrizB]
                    par = (indiceLinha, indiceColuna)
                    
                    # 3. Chama a função passando a linha, a coluna e o par ordenado (tupla)
                    # Não preciso passar o par atualmente, mas vou precisar ao criar Threads
                    future = executor.submit(trabalhador.calcularValor, linha, coluna, par) 
                    futures.append(future)

        for future in as_completed(futures):
             valor, par = future.result()
             print(f"Célula {par} concluída -> Valor: {valor}")
             coordenador.juntarMatriz(valor, par)
        
    for linha in coordenador.resultado:
        print(linha)