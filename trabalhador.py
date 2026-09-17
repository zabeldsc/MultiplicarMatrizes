class Trabalhador:
    def calcularValor(self, linha, coluna, indice):
        valor = 0
        for valorLinha, valorColuna in zip(linha, coluna):
            valor += valorLinha * valorColuna;
        return valor, indice