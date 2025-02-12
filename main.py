import random
from pysat.solvers import Solver
import numpy as np


K = [3, 5]
RAZAO = {3: {"min": 1, "max": 10}, 5: {"min": 1, "max": 20}}
INC = 0.1
QTDS_VARIAVEIS = [50, 100, 150, 200]
QTD_INSTANCIAS = 30


def gerar_instancia(qtd_variaveis, qtd_clausulas, k):
    # Caso não houvesse variáveis suficientes para completar uma cláusula, o algoritmo entraria em um loop infinito.
    if k > qtd_variaveis:
        raise ValueError("Valor de k não pode ser maior que a quantidade de variáveis.")

    # Usa-se set para ignorar duplicatas automaticamente.
    clausulas = set()

    while len(clausulas) < qtd_clausulas:
        # range retorna uma sequência de todas as variáveis.
        # random.sample escolhe aleatoriamente k elementos dessa sequência.
        # Dessa maneira, é garantido a exclusividade de cada variável em toda cláusula. 
        nova_clausula = random.sample(range(1, qtd_variaveis + 1), k)

        # Para toda variável, há 50% de chance dela ser verdadeira e 50% de chance dela ser falsa.
        # Usa-se uma tupla pois o set não suporta inserção de uma lista, por esta ser mutável.
        nova_clausula = tuple(var if random.choice([True, False]) else -var for var in nova_clausula)
        clausulas.add(nova_clausula)
    
    # Ao retornar o conjunto de cláusulas, converte todas as cláusulas (e o próprio conjunto de cláusulas) em lista.
    # Isto é visando a compatibilidade com PySAT, que espera uma lista de listas. 
    return [list(clausula) for clausula in clausulas] 


def calcular_qtd_clausulas(qtd_variaveis, razao):
    return int(qtd_variaveis * razao)
        

def main():
    for k in K:
        for razao in np.arange(RAZAO[k]["min"], RAZAO[k]["max"] + INC, INC):
            razao = round(razao, 1)
            for qtd_variaveis in QTDS_VARIAVEIS:
                instancias = list()
                qtd_instancias_sat = 0
                while len(instancias) < QTD_INSTANCIAS:
                    qtd_clausulas = calcular_qtd_clausulas(qtd_variaveis, razao)
                    nova_instancia = gerar_instancia(qtd_variaveis, qtd_clausulas, k)
                    instancias.append(nova_instancia)

                for instancia in instancias:
                    solver = Solver(name="g3")

                    for clausula in instancia:
                        solver.add_clause(clausula)
                
                    if solver.solve():
                        qtd_instancias_sat += 1
                print(f"[{k}SAT] a = {razao}, n = {qtd_variaveis}: {round(qtd_instancias_sat / QTD_INSTANCIAS * 100)}%")


main()