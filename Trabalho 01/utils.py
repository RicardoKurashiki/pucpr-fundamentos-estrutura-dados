import random as rd

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