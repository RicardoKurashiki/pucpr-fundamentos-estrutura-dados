import os
import random as rd

import pandas as pd


def generate_data(n):
    """
    Cria registros fictícios com diferentes volumes: n = {10.000, 50.000, 100.000, ...}
    Cada registro contém, por exemplo: Matrícula (9 dígitos), Nome, Salário, Código do Setor, Tempo de Serviço
    
    @param n: int
    @return: list
    """
    rd.seed(42)
    data = []
    for i in range(n):
        id = rd.randint(100000000, 999999999)
        name = f'Nome {i + 1}'
        salary = round(rd.uniform(1000, 10000), 2)
        code = f'{rd.randint(1, 1000)}'
        los = f'{rd.randint(1, 35)}'
        data.append([id, name, salary, code, los])
    return data

def sequential_search(arr, target):
    steps = 0
    for i, value in enumerate(arr):
        steps += 1
        if value[0] == target:
            return i, steps
    return -1, steps


def get_dict(sizes=[50_000, 100_000, 500_000, 1_000_000]) -> dict:
    """
    Lê os arquivos de saída e retorna um dicionário com os dados já agrupados por tamanho
    @param sizes: list
    @return: dict
    """
    output_path = "./outputs/"
    result = {}
    for fileName in os.listdir(output_path):
        if fileName.endswith(".csv"):
            df = pd.read_csv(os.path.join(output_path, fileName))
            name = fileName.replace(".csv", "")
            columns = df.columns.drop(labels=["Iteration"])
            result[name] = []
            for size in sizes:
                # Agrupa por size todas as iterações
                df_size = df[df["Size"] == size]
                data = {}
                for column in columns:
                    data[column] = df_size[column].mean()
                result[name].append(data)
    return result