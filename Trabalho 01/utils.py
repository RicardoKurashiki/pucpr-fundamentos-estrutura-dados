from tqdm import tqdm
import random as rd

def generate_data(n):
    """
    Cria registros fictícios com diferentes volumes: n = {10.000, 50.000, 100.000, ...}
    Cada registro contém, por exemplo: Matrícula (9 dígitos), Nome, Salário, Código do Setor
    
    @param n: int
    @return: list
    """
    data = []
    for i in tqdm(range(n), desc="Criando registros"):
        id = rd.randint(100000000, 999999999)
        name = f'Nome {i + 1}'
        salary = round(rd.uniform(1000, 10000), 2)
        code = f'{id:d}-{rd.randint(1, 1000)}'
        data.append([id, name, salary, code])
    print(f"Criado {n} registros")
    return data

