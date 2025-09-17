import os
import random as rd

import pandas as pd
from hashtables.tests import nome_aleatorio

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

def gen_hashtable_samples(num_elements,  **kwargs):
    
    # Valores default para funcionamento da amostragem
    config = {
        'filename': r'.\outputs\data-' + str(num_elements) + '.pkl.gz',
        'p_hat_dense': 0.5,
        'seed': 42,
        'start_range': 100_000_000,
        'final_range': 999_999_999
        }

    # Atualiza configuração conforme parâmetros
    config.update(kwargs)
    filename = config['filename']
    p_hat_dense = config['p_hat_dense']
    seed = config['seed']
    start_range = config['start_range']
    final_range = config['final_range']
    
    rd.seed(seed)


    # Define o intervalo para lista densa (com mais elementos próximos por intervalo)
    # Indica limite máximo da lista densa
    # Desse intervalo será selecionada uma amostra
    # As chaves serão geradas de 1 até dense_range_size
    p_dense = 1 - p_hat_dense # Proporção de elementos densos da lista: quanto menor, mais denso
    dense_range_size = int(num_elements * p_dense)
    
    # Calcula o número de chaves para cada intervalo
    num_dense_keys = int(dense_range_size * p_dense)
    num_sparse_keys = num_elements - num_dense_keys

    # Define o intervalo para lista esparsa (com menos elementos por intervalo)
    sparse_range_start = start_range + dense_range_size + 1
    sparse_range_end = int((num_elements - dense_range_size) ** 2) if final_range <= (sparse_range_start + num_sparse_keys) else final_range
    
    
    # Gera as chaves aleatórias
    dense_keys = rd.sample(range(start_range, start_range + dense_range_size), num_dense_keys)
    sparse_keys = rd.sample(range(sparse_range_start, sparse_range_end + 1), num_sparse_keys)
    
    all_keys = dense_keys + sparse_keys
    rd.shuffle(all_keys)

    data = []
    nomes_aleatorios = nome_aleatorio.gerar_nomes_aleatorios(num_elements, seed)
    for i, k in enumerate(all_keys):
        id = all_keys[i]
        name = nomes_aleatorios[i]
        salary = round(rd.uniform(1000, 10000), 2)
        code = f'{rd.randint(1, 1000)}'
        los = f'{rd.randint(1, 35)}'
        data.append([id, name, salary, code, los])
    
    to_gzip(data, filename=filename)
    print('Listas de dados salvas em ')
    return data

def to_gzip(obj, filename:str):
    import gzip, pickle
    with gzip.open(filename, 'wb') as f:
        pickle.dump(obj, f)

def from_gzip(filename:str):
    import gzip, pickle
    with gzip.open(filename, 'rb') as f:
        return pickle.load(f)

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