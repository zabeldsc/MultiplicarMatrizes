"""Trabalhador (Parte 1): processo que recebe uma linha e uma coluna e devolve o produto escalar."""
import time
from matrizes import ATRASO


class Trabalhador:
    def calcularValor(self, linha, coluna, indice):
        """Produto escalar entre `linha` e `coluna`. Devolve (valor, indice)."""
        time.sleep(ATRASO)  # simula custo de processamento
        valor = 0
        for valor_linha, valor_coluna in zip(linha, coluna):
            valor += valor_linha * valor_coluna
        return valor, indice


def processo_trabalhador(id_trabalhador, fila_tarefas, fila_resultados):
    """Laço principal de um processo trabalhador.

    Recebe mensagens (linha, coluna, par) pela `fila_tarefas` e devolve
    (id_trabalhador, valor, par) pela `fila_resultados`.
    A mensagem None é o sinal de encerramento.
    """
    trabalhador = Trabalhador()
    while True:
        tarefa = fila_tarefas.get()          # bloqueia até chegar uma mensagem
        if tarefa is None:
            break
        linha, coluna, par = tarefa
        valor, par = trabalhador.calcularValor(linha, coluna, par)
        fila_resultados.put((id_trabalhador, valor, par))