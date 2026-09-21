#!/bin/bash
# Parte 1
python3 coordenador.py

# Parte 2
python3 -m Pyro5.nameserver > /dev/null 2>&1 &
sleep 2
python3 servidor_trabalhador.py 1 > /dev/null 2>&1 &
python3 servidor_trabalhador.py 2 > /dev/null 2>&1 &
python3 servidor_trabalhador.py 3 > /dev/null 2>&1 &
sleep 2
python3 coordenador_rpc.py 3

# encerra Name Server e trabalhadores
kill $(jobs -p)