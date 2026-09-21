"""Coordenador (Parte 2): invoca métodos remotos via middleware (Pyro5).

Não há filas nem mensagens manuais: o coordenador chama
`proxy.calcularValor(...)` como se fosse uma função local.
"""
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import Pyro5.api

from matrizes import (MATRIZ_A, MATRIZ_B, extrair_coluna, criar_resultado_vazio,
                      imprimir_matriz, multiplicar_sequencial)


class CoordenadorRPC:
    def __init__(self, num_trabalhadores=3):
        self.matrizA = MATRIZ_A
        self.matrizB = MATRIZ_B
        self.resultado = criar_resultado_vazio(self.matrizA, self.matrizB)
        ns = Pyro5.api.locate_ns()
        # Descobre as URIs dos trabalhadores pelo Name Server
        self.uris = [ns.lookup(f"trabalhador.{k + 1}") for k in range(num_trabalhadores)]

    def juntarMatriz(self, valor, par):
        self.resultado[par[0]][par[1]] = valor

    def _gerar_tarefas(self):
        n = 0
        for i in range(len(self.matrizA)):
            for j in range(len(self.matrizB[0])):
                yield self.uris[n % len(self.uris)], self.matrizA[i], extrair_coluna(self.matrizB, j), (i, j)
                n += 1

    @staticmethod
    def _chamar(uri, linha, coluna, par):
        # Um Proxy por thread (proxies do Pyro não devem ser compartilhados entre threads)
        with Pyro5.api.Proxy(uri) as trabalhador:
            valor, par = trabalhador.calcularValor(linha, coluna, par)   # chamada remota
        return valor, tuple(par)

    def executar_sincrono(self):
        """Uma chamada remota por vez, aguardando cada retorno."""
        for uri, linha, coluna, par in self._gerar_tarefas():
            valor, par = self._chamar(uri, linha, coluna, par)
            print(f"[RPC SÍNCRONO] célula {par} = {valor}")
            self.juntarMatriz(valor, par)

    def executar_assincrono(self):
        """Várias chamadas remotas simultâneas (uma thread por chamada)."""
        with ThreadPoolExecutor(max_workers=len(self.uris) * 2) as ex:
            futuros = [ex.submit(self._chamar, *t) for t in self._gerar_tarefas()]
            for f in as_completed(futuros):
                valor, par = f.result()
                print(f"[RPC ASSÍNCRONO] célula {par} = {valor}")
                self.juntarMatriz(valor, par)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    esperado = multiplicar_sequencial(MATRIZ_A, MATRIZ_B)
    for nome, metodo in (("SÍNCRONA", "executar_sincrono"), ("ASSÍNCRONA", "executar_assincrono")):
        print(f"\n===== RPC (Pyro5) - chamada {nome} =====")
        coord = CoordenadorRPC(n)
        inicio = time.perf_counter()
        getattr(coord, metodo)()
        tempo = time.perf_counter() - inicio
        imprimir_matriz(coord.resultado, f"Matriz resultante (RPC {nome.lower()})")
        print(f"Tempo: {tempo:.2f}s | Correto: {coord.resultado == esperado}")