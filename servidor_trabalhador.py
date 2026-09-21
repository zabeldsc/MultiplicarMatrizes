"""Trabalhador remoto (Parte 2): objeto exposto via Pyro5.

Uso:  python servidor_trabalhador.py <id>
Cada instância registra-se no Name Server como "trabalhador.<id>".
"""
import sys
import time
import Pyro5.api

from matrizes import ATRASO


@Pyro5.api.expose
class TrabalhadorRemoto:
    def calcularValor(self, linha, coluna, indice):
        """Método REMOTO: produto escalar entre linha e coluna."""
        time.sleep(ATRASO)
        valor = sum(a * b for a, b in zip(linha, coluna))
        return valor, indice   # o Pyro serializa a tupla como lista


if __name__ == "__main__":
    id_t = sys.argv[1] if len(sys.argv) > 1 else "1"
    daemon = Pyro5.api.Daemon()                      # servidor de requisições
    ns = Pyro5.api.locate_ns()                       # localiza o Name Server
    uri = daemon.register(TrabalhadorRemoto())       # registra o objeto
    ns.register(f"trabalhador.{id_t}", uri)          # publica o nome
    print(f"Trabalhador {id_t} pronto: {uri}")
    daemon.requestLoop()