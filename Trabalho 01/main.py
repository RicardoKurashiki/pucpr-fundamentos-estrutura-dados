import argparse
import csv
import os
import random as rd
import tracemalloc

import matplotlib.pyplot as plt
import psutil as p
from avltree import AVLTree
from constants import METRICS
from hashtable import HashTable
from unbaltree import UnBalTree
from utils import generate_data, get_dict, sequential_search

parser = argparse.ArgumentParser()
parser.add_argument("--skip", action="store_true")
parser.add_argument("--plot", action="store_true")
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
    metrics = {}  # dicionário para coleta das métricas
    # Objeto Process que representa o nosso script atual
    process = p.Process(os.getpid())

    # --- BUSCA POR AMOSTRAGEM ---
    # Definimos o tamanho da amostra como 1% do total de dados.
    # Usamos max(1, ...) para garantir que, mesmo para N muito pequeno, testamos pelo menos 1 elemento.
    sample_percent = 0.01
    sample_size = max(1, int(len(data) * sample_percent))
    search_sample = rd.sample(data, sample_size)

    # Busca Sequencial
    tracemalloc.start()
    cpu_before_search = process.cpu_times()

    for item_to_search in search_sample:
        id_to_search = item_to_search[0]
        _, seq_search_steps = sequential_search(data, id_to_search)

    cpu_after_search = process.cpu_times()
    memoryusage_search, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    metrics["Memory Usage (Peak Bytes)"] = peak_mem
    metrics["Memory Usage (Bytes)"] = memoryusage_search
    metrics["Steps"] = seq_search_steps
    metrics["Search CPU Time (s)"] = (
        cpu_after_search.user - cpu_before_search.user
    ) + (cpu_after_search.system - cpu_before_search.system)

    return metrics


def test_avltree_lifecycle(data):
    metrics = {}  # dicionário para coleta das métricas
    # Objeto Process que representa o nosso script atual
    process = p.Process(os.getpid())

    # FASE 1: INSERÇÃO
    tracemalloc.start()
    # Mede o tempo de CPU inicial
    cpu_before_insert = process.cpu_times()

    tree = AVLTree(key=lambda registro: registro[0])
    for item in data:
        tree.insert(item)

    cpu_after_insert = process.cpu_times()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()  # Paramos o tracemalloc aqui, pois a estrutura já está criada.

    # Coleta de métricas da Fase 1
    metrics["Memory Usage (Peak Bytes)"] = peak_mem
    metrics["Insertion CPU Time (s)"] = (
        cpu_after_insert.user - cpu_before_insert.user
    ) + (cpu_after_insert.system - cpu_before_insert.system)
    metrics["Rotation Events"] = tree.rotation_count
    if tree.root:
        metrics["Tree Height"] = tree.root.height

    # --- FASE 2: BUSCA POR AMOSTRAGEM ---
    cpu_before_search = process.cpu_times()

    total_depth = 0
    max_depth = 0
    # Definimos o tamanho da amostra como 1% do total de dados.
    # Usamos max(1, ...) para garantir que, mesmo para N muito pequeno, testamos pelo menos 1 elemento.
    sample_percent = 0.01
    sample_size = max(1, int(len(data) * sample_percent))

    search_sample = rd.sample(data, sample_size)

    for item_to_search in search_sample:
        key_to_search = item_to_search[0]
        _, search_metrics = tree.search(key_to_search)
        max_depth = max(max_depth, search_metrics["Search Depth"])
        total_depth += search_metrics["Search Depth"]

    cpu_after_search = process.cpu_times()

    # Coleta de métricas da Fase 2
    metrics["Search CPU Time (s)"] = (
        cpu_after_search.user - cpu_before_search.user
    ) + (cpu_after_search.system - cpu_before_search.system)
    metrics["Average Search Depth"] = total_depth / sample_size
    metrics["Max Search Depth"] = max_depth

    return metrics


def test_unbaltree_lifecycle(data):
    metrics = {}  # dicionário para coleta das métricas
    # Objeto Process que representa o nosso script atual
    process = p.Process(os.getpid())

    # FASE 1: INSERÇÃO
    tracemalloc.start()
    # Mede o tempo de CPU inicial
    cpu_before_insert = process.cpu_times()

    tree = UnBalTree(key=lambda registro: registro[0])
    for item in data:
        tree.insert(item)

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

    # --- FASE 2: BUSCA POR AMOSTRAGEM ---
    cpu_before_search = process.cpu_times()

    total_depth = 0
    max_depth = 0
    # Definimos o tamanho da amostra como 1% do total de dados.
    # Usamos max(1, ...) para garantir que, mesmo para N muito pequeno, testamos pelo menos 1 elemento.
    sample_percent = 0.01
    sample_size = max(1, int(len(data) * sample_percent))

    search_sample = rd.sample(data, sample_size)

    for item_to_search in search_sample:
        key_to_search = item_to_search[0]
        _, search_metrics = tree.search(key_to_search)
        max_depth = max(max_depth, search_metrics["Search Depth"])
        total_depth += search_metrics["Search Depth"]

    cpu_after_search = process.cpu_times()

    # Coleta de métricas da Fase 2
    metrics["Search CPU Time (s)"] = (
        cpu_after_search.user - cpu_before_search.user
    ) + (cpu_after_search.system - cpu_before_search.system)
    metrics["Average Search Depth"] = total_depth / sample_size
    metrics["Max Search Depth"] = max_depth

    return metrics


def hash_test(data):
    m = [100, 1000, 5000]
    for hash_size in m:
        print(f"Inserting {len(data)} into {hash_size} Hash Table")
        metrics = {}  # dicionário para coleta das métricas
        # Objeto Process que representa o nosso script atual
        process = p.Process(os.getpid())

        # FASE 1: INSERÇÃO
        tracemalloc.start()
        # Mede o tempo de CPU inicial
        cpu_before_insert = process.cpu_times()

        hash_table = HashTable(hash_size)
        for item in data:
            hash_table.insert(item[0], item[1:])

        cpu_after_insert = process.cpu_times()
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()  # Paramos o tracemalloc aqui, pois a estrutura já está criada.

        # Coleta de métricas da Fase 1
        metrics["M parameter"] = hash_size
        metrics["Memory Usage (Peak Bytes)"] = peak_mem
        metrics["Insertion CPU Time (s)"] = (
            cpu_after_insert.user - cpu_before_insert.user
        ) + (cpu_after_insert.system - cpu_before_insert.system)

        # --- FASE 2: BUSCA POR AMOSTRAGEM ---
        cpu_before_search = process.cpu_times()

        total_search_steps = 0
        max_depth = 0
        # Definimos o tamanho da amostra como 1% do total de dados.
        # Usamos max(1, ...) para garantir que, mesmo para N muito pequeno, testamos pelo menos 1 elemento.
        sample_percent = 0.01
        sample_size = max(1, int(len(data) * sample_percent))

        search_sample = rd.sample(data, sample_size)
        search_iteration = 0
        for item_to_search in search_sample:
            search_iteration += 1
            key_to_search = item_to_search[0]
            _, search_metrics = hash_table.search(key_to_search)
            total_search_steps += search_metrics["Search Steps"]

        cpu_after_search = process.cpu_times()

        # Coleta de métricas da Fase 2
        metrics["Search CPU Time (s)"] = (
            cpu_after_search.user - cpu_before_search.user
        ) + (cpu_after_search.system - cpu_before_search.system)
        metrics["Average Search Depth"] = total_search_steps / sample_size
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
    algorithms: list = ["linear_array", "avl_tree", "regular_tree"],
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
    plot = args.plot
    skip = args.skip
    if not skip:
        print("Rodando experimentos...")
        for size in sizes:
            """ Cada conjunto de dados de tamanho N é gerado uma única vez pois fixamos a semente aleatória para garantir a
            reprodutibilidade do experimento. Caso se deseje uma ideia da melhor performance para o "caso médio geral", poderia
            ser removida a inicialização da semente aleatória, e a geração do conjunto de dados seria feita no loop interno
            """
            data = generate_data(size)
            for i in range(iterations):
                # array_metrics = linear_array_test(data)
                # compute_and_log_metrics(array_metrics, "linear_array", i, size)
                hash_metrics = hash_test(data)
                compute_and_log_metrics(hash_metrics, "hash_table", i, size)
                # unbaltree_metrics = test_unbaltree_lifecycle(data)
                # compute_and_log_metrics(unbaltree_metrics, "regular_tree", i, size)
                # avl_metrics = test_avltree_lifecycle(data)
                # compute_and_log_metrics(avl_metrics, "avl_tree", i, size)

    if plot:
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
    print("Finalizado!")


if __name__ == "__main__":
    main()
