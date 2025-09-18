import argparse
import pandas as pd
import csv
import os
import random as rd
import tracemalloc

import matplotlib.pyplot as plt
import psutil as p
from avltree import AVLTree
from constants import METRICS
from hashtableextended import HashTable
from unbaltree import UnBalTree
from utils import generate_data, get_dict, sequential_search, gen_hashtable_samples

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--no-test", action="store_true")
parser.add_argument("--array", action="store_true")
parser.add_argument("--hash", action="store_true")
parser.add_argument("--tree", action="store_true")
parser.add_argument("-a", "--all", action="store_true")
parser.add_argument("-p", "--no-plot", action="store_true")
args = parser.parse_args()


def compute_and_log_metrics(metrics, name, iteration, size):
    """
    Recebe um dicionário de métricas e o salva em um arquivo CSV.
    O cabeçalho é escrito automaticamente apenas se o arquivo não existir.
    """

    # Define um nome de arquivo único por algoritmo
    filename = f"./outputs/{name}.csv"
    os.makedirs("./outputs/", exist_ok=True)

    # Prepara a linha de dados a ser escrita
    # Começa com os parâmetros do teste e depois adiciona todas as métricas coletadas
    row_data = {
        "Size": size,
        "Iteration": iteration,
        **metrics,  # Desempacota o dicionário de métricas na linha
    }

    # Define o cabeçalho a partir das chaves do nosso dicionário de dados
    header = row_data.keys()

    # Verifica se o arquivo já existe para decidir se escreve o cabeçalho
    file_exists = os.path.exists(filename)
    # Abre o arquivo em modo 'append' (a) e escreve a nova linha
    # newline='' é importante para evitar linhas em branco no CSV
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)

        # Se o arquivo não existe, escreve o cabeçalho
        if not file_exists:
            writer.writeheader()

        # Escreve a linha de dados
        writer.writerow(row_data)


def linear_array_test(data):
    print(f"Inserting {len(data)} into Linear Array")
    metrics = {}  # dicionário para coleta das métricas
    # Objeto Process que representa o nosso script atual
    process = p.Process(os.getpid())

    # FASE 1: INSERÇÃO
    tracemalloc.start()
    # Mede o tempo de CPU inicial
    cpu_before_insert = process.cpu_times()

    total_insert_steps = 0
    linear_array = []
    for item in data:
        linear_array[len(linear_array):] = item
        total_insert_steps += 1

    cpu_after_insert = process.cpu_times()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()  # Paramos o tracemalloc aqui, pois a estrutura já está criada.

    # Coleta de métricas da Fase 1
    metrics["Memory Usage (Peak Bytes)"] = peak_mem
    metrics["Insertion CPU Time (s)"] = (
        cpu_after_insert.user - cpu_before_insert.user
    ) + (cpu_after_insert.system - cpu_before_insert.system)
    metrics["Total Insertion Steps"] = total_insert_steps

    # --- BUSCA POR AMOSTRAGEM ---
    # Definimos o tamanho da amostra como 1% do total de dados.
    # Usamos max(1, ...) para garantir que, mesmo para N muito pequeno, testamos pelo menos 1 elemento.
    #sample_percent = 0.01
    #sample_size = max(1, int(len(data) * sample_percent))
    sample_size = 512
    search_sample = rd.sample(data, sample_size)
    total_search_steps = 0

    # Busca Sequencial
    tracemalloc.start()
    cpu_before_search = process.cpu_times()

    for item_to_search in search_sample:
        id_to_search = item_to_search[0]
        _, seq_search_steps = sequential_search(data, id_to_search)
        total_search_steps += seq_search_steps

    cpu_after_search = process.cpu_times()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    metrics["Average Search Steps"] = total_search_steps / sample_size
    metrics["Search CPU Time (s)"] = (
        cpu_after_search.user - cpu_before_search.user
    ) + (cpu_after_search.system - cpu_before_search.system)

    return metrics


def test_avltree_lifecycle(data):
    print(f"Inserting {len(data)} into AVL Tree")
    metrics = {}  # dicionário para coleta das métricas
    # Objeto Process que representa o nosso script atual
    process = p.Process(os.getpid())

    # FASE 1: INSERÇÃO
    tracemalloc.start()
    # Mede o tempo de CPU inicial
    cpu_before_insert = process.cpu_times()

    total_insert_steps = 0
    tree = AVLTree(key=lambda registro: registro[0])
    for item in data:
        insert_metrics = tree.insert(item)
        total_insert_steps += insert_metrics["Insert Steps"]

    cpu_after_insert = process.cpu_times()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()  # Paramos o tracemalloc aqui, pois a estrutura já está criada.

    # Coleta de métricas da Fase 1
    metrics["Memory Usage (Peak Bytes)"] = peak_mem
    metrics["Insertion CPU Time (s)"] = (
        cpu_after_insert.user - cpu_before_insert.user
    ) + (cpu_after_insert.system - cpu_before_insert.system)
    if tree.root:
        metrics["Rotation Events"] = tree.rotation_count
        metrics["Tree Height"] = tree.root.height
        metrics["Total Insertion Steps"] = total_insert_steps

    # --- FASE 2: BUSCA POR AMOSTRAGEM ---

    total_depth_for_one_run = 0
    max_depth_for_one_run = 0
    # Definimos o tamanho da amostra como 1% do total de dados.
    # Usamos max(1, ...) para garantir que, mesmo para N muito pequeno, testamos pelo menos 1 elemento.
    #sample_percent = 0.01
    #sample_size = max(1, int(len(data) * sample_percent))
    sample_size = 512
    search_sample = rd.sample(data, sample_size)

    # Define o número de repetições para amplificar a carga de trabalho - várias medições com valor zero sem essas repetições
    search_repetitions = 20

    cpu_before_search = process.cpu_times()

    for i in range(search_repetitions):
        for item_to_search in search_sample:
            key_to_search = item_to_search[0]
            _, search_metrics = tree.search(key_to_search)
            # As métricas de profundidade só precisam ser calculadas na primeira repetição
            if i == 0:
                total_depth_for_one_run += search_metrics["Search Steps"]
                max_depth_for_one_run = max(max_depth_for_one_run, search_metrics["Search Steps"])


    cpu_after_search = process.cpu_times()

    # Coleta de métricas da Fase 2
    total_cpu_time = (cpu_after_search.user - cpu_before_search.user) + (
                cpu_after_search.system - cpu_before_search.system)
    # Normaliza o tempo de CPU pelo número de repetições para obter a média precisa
    metrics["Search CPU Time (s)"] = total_cpu_time / search_repetitions
    # As métricas de profundidade são baseadas em uma única execução da amostra
    if search_sample:
        metrics["Average Search Steps"] = total_depth_for_one_run / len(search_sample)
    else:
        metrics["Average Search Steps"] = 0
    metrics["Max Search Steps"] = max_depth_for_one_run

    return metrics


def test_unbaltree_lifecycle(data):
    print(f"Inserting {len(data)} into Unbalanced Tree")
    metrics = {}  # dicionário para coleta das métricas
    # Objeto Process que representa o nosso script atual
    process = p.Process(os.getpid())

    # FASE 1: INSERÇÃO
    tracemalloc.start()
    # Mede o tempo de CPU inicial
    cpu_before_insert = process.cpu_times()

    total_insert_steps = 0
    tree = UnBalTree(key=lambda registro: registro[0])
    for item in data:
        insert_metrics = tree.insert(item)
        total_insert_steps += insert_metrics["Insert Steps"]

    cpu_after_insert = process.cpu_times()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()  # Paramos o tracemalloc aqui, pois a estrutura já está criada.

    # Coleta de métricas da Fase 1
    metrics["Memory Usage (Peak Bytes)"] = peak_mem
    metrics["Insertion CPU Time (s)"] = (
        cpu_after_insert.user - cpu_before_insert.user
    ) + (cpu_after_insert.system - cpu_before_insert.system)
    if tree.root:
        metrics["Tree Height"] = tree.root.height
        metrics["Total Insertion Steps"] = total_insert_steps

    # --- FASE 2: BUSCA POR AMOSTRAGEM ---
    total_depth_for_one_run = 0
    max_depth_for_one_run = 0
    # Definimos o tamanho da amostra como 1% do total de dados.
    # Usamos max(1, ...) para garantir que, mesmo para N muito pequeno, testamos pelo menos 1 elemento.
    #sample_percent = 0.01
    #sample_size = max(1, int(len(data) * sample_percent))
    sample_size = 512
    search_sample = rd.sample(data, sample_size)
    search_repetitions = 20

    cpu_before_search = process.cpu_times()

    for i in range(search_repetitions):
        for item_to_search in search_sample:
            key_to_search = item_to_search[0]
            _, search_metrics = tree.search(key_to_search)
            if i == 0:
                total_depth_for_one_run += search_metrics["Search Steps"]
                max_depth_for_one_run = max(max_depth_for_one_run, search_metrics["Search Steps"])

    cpu_after_search = process.cpu_times()

    # Coleta de métricas da Fase 2
    total_cpu_time = (cpu_after_search.user - cpu_before_search.user) + (
                cpu_after_search.system - cpu_before_search.system)
    metrics["Search CPU Time (s)"] = total_cpu_time / search_repetitions

    if search_sample:
        metrics["Average Search Steps"] = total_depth_for_one_run / len(search_sample)
    else:
        metrics["Average Search Steps"] = 0
    metrics["Max Search Steps"] = max_depth_for_one_run

    return metrics


def hash_test(data, m, hash_function):

    print(f"Inserting {len(data)} into {hash_function} Hash Table ({m})")
    metrics = {}  # dicionário para coleta das métricas
    # Objeto Process que representa o nosso script atual
    process = p.Process(os.getpid())

    # FASE 1: INSERÇÃO
    tracemalloc.start()
    # Mede o tempo de CPU inicial
    cpu_before_insert = process.cpu_times()

    hash_table = HashTable(m, hash_function)
    total_insert_steps = 0
    for item in data:
        insert_metrics = hash_table.insert(item[0], item[1:])
        total_insert_steps += insert_metrics['Insert Steps']

    cpu_after_insert = process.cpu_times()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()  # Paramos o tracemalloc aqui, pois a estrutura já está criada.

    # Coleta de métricas da Fase 1
    metrics["M parameter"] = m
    metrics["Hash Function"] = hash_function
    metrics["Memory Usage (Peak Bytes)"] = peak_mem
    metrics["Insertion CPU Time (s)"] = (
        cpu_after_insert.user - cpu_before_insert.user
    ) + (cpu_after_insert.system - cpu_before_insert.system)
    metrics["Total Insertion Steps"] = total_insert_steps

    structural_metrics = hash_table.get_structural_metrics()
    metrics.update(structural_metrics)

    # --- FASE 2: BUSCA POR AMOSTRAGEM ---
    cpu_before_search = process.cpu_times()

    total_search_steps = 0
    sample_size = 512
    if len(data) < sample_size:
        search_sample = data
    else:
        search_sample = rd.sample(data, sample_size)

    for item_to_search in search_sample:
        key_to_search = item_to_search[0]
        _, search_metrics = hash_table.search(key_to_search)
        total_search_steps += search_metrics["Search Steps"]

    cpu_after_search = process.cpu_times()

    # Coleta de métricas da Fase 2
    metrics["Search CPU Time (s)"] = (
        cpu_after_search.user - cpu_before_search.user
    ) + (cpu_after_search.system - cpu_before_search.system)
    metrics["Average Search Steps"] = total_search_steps / sample_size

    # Salvar dados de distribuição dos buckets para geração de um histograma
    bucket_lengths = [len(bucket) for bucket in hash_table.table]
    # Usamos o pandas para contar a frequência de cada tamanho de bucket
    value_counts = pd.Series(bucket_lengths).value_counts().reset_index()
    value_counts.columns = ['Bucket Size', 'Frequency']

    # Adiciona colunas de identificação para esta execução específica
    value_counts['Size'] = len(data)
    value_counts['M parameter'] = m
    value_counts['Hash Function'] = hash_function

    # Salva esses dados em um arquivo CSV separado
    dist_filename = './outputs/hash_distribution.csv'
    file_exists = os.path.exists(dist_filename)
    # 'a' para append, para não sobrescrever os resultados de outras execuções
    value_counts.to_csv(dist_filename, mode='a', header=not file_exists, index=False)

    return metrics

    # EXEMPLO DE EXTENSIBILIDADE:
    # Suponha que o search da HashTable retorne o número de colisões encontradas
    # _, metrics = hash_table.search(data[len(data) // 2][0])
    # return metrics # -> retornaria algo como {'Collisions': 1}

    # Por enquanto, não faremos isso
    # hash_table.search(data[len(data) // 2][0])


def plot_data_comparison(
    data: dict,
    sizes: list = [50_000, 100_000, 500_000, 1_000_000],
    algorithms: list = ["linear_array", "avl_tree", "regular_tree", "hash_table"],
    output_path: str = "./outputs/charts/",
):
    def get_progression(algorithm: str, metric: str):
        Y = []
        for size_result in data[algorithm]:
            if metric in size_result:
                Y.append(size_result[metric])
        return Y

    plot_data = {}
    for metric in METRICS:
        plot_data[metric] = METRICS[metric].copy()
        for algorithm in algorithms:
            plot_data[metric][algorithm] = get_progression(algorithm, metric)

    # Plotar os dados como comparação entre algoritmos
    for metric in METRICS:
        plt.figure(figsize=(10, 6))

        # Converter tamanhos para formato mais legível (em milhares)
        x_sizes = [size / 1000 for size in sizes]  # Converter para milhares

        # Para cada algoritmo, plotar com interpolação suave
        algorithms = [
            ("linear_array", "Array Linear", "blue"),
            ("avl_tree", "Árvore Balanceada", "green"),
            ("regular_tree", "Árvore Desbalanceada", "red"),
        ]

        fig = plt.figure(figsize=(10, 6))

        for algo_key, algo_label, color in algorithms:
            if algo_key in plot_data[metric] and len(plot_data[metric][algo_key]) > 0:
                y_values = plot_data[metric][algo_key]
                plt.plot(
                    x_sizes,
                    y_values,
                    color=color,
                    linewidth=2,
                    label=algo_label,
                    alpha=0.7,
                )

        # Configurações do gráfico
        plt.title(METRICS[metric]["title"], fontsize=14, fontweight="bold")
        plt.xlabel("Tamanho do Conjunto de Dados (x1000)", fontsize=12)
        ylabel = METRICS[metric]["ylabel"]
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(x_sizes, [f"{int(x)}k" for x in x_sizes])
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=10, loc="best")
        plt.tight_layout()

        # Salvar gráfico
        os.makedirs(output_path, exist_ok=True)
        fig.savefig(f"{output_path}/{metric}.png")
        plt.close(fig)


def main():
    rd.seed(42)
    sizes = [50_000, 100_000, 500_000, 1_000_000]
    iterations = 5
    no_test = args.no_test
    no_plot = args.no_plot
    test_array = args.array
    test_hash = args.hash
    test_tree = args.tree
    test_all = args.all
    if not no_test:
        print("Rodando experimentos...")
        for size in sizes:
            """ Cada conjunto de dados de tamanho N é gerado uma única vez pois fixamos a semente aleatória para garantir a
            reprodutibilidade do experimento. Caso se deseje uma ideia da melhor performance para o "caso médio geral", poderia
            ser removida a inicialização da semente aleatória, e a geração do conjunto de dados seria feita no loop interno
            """
            data = gen_hashtable_samples(size)
            for i in range(iterations):
                if test_array or test_all:
                    array_metrics = linear_array_test(data)
                    compute_and_log_metrics(array_metrics, "linear_array", i, size)
                if test_hash or test_all:
                    m = [100, 1000, 5000]
                    hash_functions = ['modulo', 'folding', 'golden_ratio']
                    for hash_size in m:
                        for function in hash_functions:
                            hash_metrics = hash_test(data, hash_size, function)
                            hash_metrics['Hash Function'] = function
                            compute_and_log_metrics(hash_metrics, "hash_table", i, size)
                if test_tree or test_all:
                    unbaltree_metrics = test_unbaltree_lifecycle(data)
                    compute_and_log_metrics(unbaltree_metrics, "regular_tree", i, size)
                    avl_metrics = test_avltree_lifecycle(data)
                    compute_and_log_metrics(avl_metrics, "avl_tree", i, size)

    if not no_plot:
        print("Plotando dados...")
        dict = get_dict(sizes)
        plot_data_comparison(
            dict,
            sizes=sizes,
            algorithms=["linear_array", "avl_tree", "regular_tree"],
            output_path="./outputs/charts/comparison/all/",
        )
        plot_data_comparison(
            dict,
            sizes=sizes,
            algorithms=["avl_tree", "regular_tree"],
            output_path="./outputs/charts/comparison/trees/",
        )
        plot_data_comparison(
            dict,
            sizes=sizes,
            algorithms=["avl_tree"],
            output_path="./outputs/charts/avl_tree/",
        )
        plot_data_comparison(
            dict,
            sizes=sizes,
            algorithms=["regular_tree"],
            output_path="./outputs/charts/regular_tree/",
        )
        plot_data_comparison(
            dict,
            sizes=sizes,
            algorithms=["linear_array"],
            output_path="./outputs/charts/linear_array/",
        )
        plot_data_comparison(
            dict,
            sizes=sizes,
            algorithms=["hash_table"],
            output_path="./outputs/charts/linear_array/",
        )
    print("Finalizado!")


if __name__ == "__main__":
    main()
