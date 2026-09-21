"""Coordenador (Parte 1): comunicação DIRETA entre processos (multiprocessing).

Cada trabalhador é um processo separado (não uma thread) que se comunica com o
coordenador por troca de mensagens (filas). Duas estratégias:
  - síncrona:  envia UMA tarefa e espera a resposta antes de enviar a próxima;
  - assíncrona: envia TODAS as tarefas e coleta as respostas conforme chegam.
"""
import time
from multiprocessing import Process, Queue

from matrizes import (MATRIZ_A, MATRIZ_B, extrair_coluna, criar_resultado_vazio,
                      imprimir_matriz, multiplicar_sequencial)
from trabalhador import processo_trabalhador


class Coordenador:
    def __init__(self, num_trabalhadores=3):
        self.matrizA = MATRIZ_A
        self.matrizB = MATRIZ_B
        self.resultado = criar_resultado_vazio(self.matrizA, self.matrizB)
        self.num_trabalhadores = num_trabalhadores

    def juntarMatriz(self, valor, par):
        """Coloca o valor recebido na posição (linha, coluna) da matriz resultante."""
        self.resultado[par[0]][par[1]] = valor

    def _gerar_tarefas(self):
        """Gera (linha de A, coluna de B, par) para cada célula do resultado."""
        for i in range(len(self.matrizA)):
            for j in range(len(self.matrizB[0])):
                yield self.matrizA[i], extrair_coluna(self.matrizB, j), (i, j)

    def _iniciar_trabalhadores(self):
        """Cria os processos trabalhadores, cada um com sua fila de entrada."""
        filas_tarefas = [Queue() for _ in range(self.num_trabalhadores)]
        fila_resultados = Queue()  # fila única de respostas
        processos = [Process(target=processo_trabalhador, args=(k, filas_tarefas[k], fila_resultados))
                     for k in range(self.num_trabalhadores)]
        for p in processos:
            p.start()
        return processos, filas_tarefas, fila_resultados

    def _encerrar(self, processos, filas_tarefas):
        for fila in filas_tarefas:
            fila.put(None)
        for p in processos:
            p.join()

    # ------------------------------------------------------------------ SÍNCRONO
    def executar_sincrono(self):
        processos, filas, fila_res = self._iniciar_trabalhadores()
        for n, (linha, coluna, par) in enumerate(self._gerar_tarefas()):
            k = n % self.num_trabalhadores          # round-robin
            filas[k].put((linha, coluna, par))      # envia a tarefa...
            id_t, valor, par = fila_res.get()       # ...e BLOQUEIA até a resposta chegar
            print(f"[SÍNCRONO] Trabalhador {id_t} -> célula {par} = {valor}")
            self.juntarMatriz(valor, par)
        self._encerrar(processos, filas)

    # ---------------------------------------------------------------- ASSÍNCRONO
    def executar_assincrono(self):
        processos, filas, fila_res = self._iniciar_trabalhadores()
        total = 0
        for n, (linha, coluna, par) in enumerate(self._gerar_tarefas()):
            filas[n % self.num_trabalhadores].put((linha, coluna, par))  # não espera resposta
            total += 1
        for _ in range(total):                      # coleta na ordem de chegada
            id_t, valor, par = fila_res.get()
            print(f"[ASSÍNCRONO] Trabalhador {id_t} -> célula {par} = {valor}")
            self.juntarMatriz(valor, par)
        self._encerrar(processos, filas)


if __name__ == "__main__":
    esperado = multiplicar_sequencial(MATRIZ_A, MATRIZ_B)

    for nome, metodo in (("SÍNCRONA", "executar_sincrono"), ("ASSÍNCRONA", "executar_assincrono")):
        print(f"\n===== Comunicação {nome} =====")
        coord = Coordenador(num_trabalhadores=3)
        inicio = time.perf_counter()
        getattr(coord, metodo)()
        tempo = time.perf_counter() - inicio
        imprimir_matriz(coord.resultado, f"Matriz resultante ({nome.lower()})")
        print(f"Tempo: {tempo:.2f}s | Correto: {coord.resultado == esperado}")